#!/usr/bin/env -S poetry run python3

from enum import Enum
import typer
from typing import Annotated
import tomllib
from pathlib import Path
import subprocess
import shlex


BT_SCRIPT = Path(__file__).parent / "heat.bt"
BT_EXCLUDE_GC_SCRIPT = Path(__file__).parent / "heat-other.bt"
PROJECT_ROOT = (Path(__file__).parent / ".." / "..").resolve()


def build_openjdk():
    typer.echo("Building...")
    with open(PROJECT_ROOT / ".cargo" / "config.toml", "rb") as f:
        config = tomllib.load(f)
    if config.get("build", {}).get("rustflags", []) != ["-C", "force-frame-pointers=yes"]:
        typer.echo("Please add the following to .cargo/config.toml:")
        typer.echo("[build]")
        typer.echo('rustflags = ["-C", "force-frame-pointers=yes"]')
        raise typer.Exit(1)
    with open(PROJECT_ROOT / "mmtk-openjdk" / "mmtk" / "Cargo.toml", "rb") as f:
        cargo = tomllib.load(f)
    if cargo.get("profile", {}).get("release", {}).get("debug", False) != True:
        typer.echo("Please add the following to [profile.release] section in mmtk-openjdk/mmtk/Cargo.toml:")
        typer.echo("debug = true")
        raise typer.Exit(1)
    subprocess.check_call(["poetry", "run", "mmtk-jdk", "build", "--release"], cwd=PROJECT_ROOT)


class GC(str, Enum):
    ix = "ix"
    lxr = "lxr"
    g1 = "g1"
    par = "par"
    shen = "shen"
    z = "z"


DEFAULT_HEAPS = {
    "lusearch": "512M",
    "h2": "2G",
    "kafka": "512M",
}


def main(
    gc: Annotated[GC, typer.Option()],
    heap: str | None = None,
    bench: str = "lusearch",
    build: bool = False,
    iter: Annotated[int, typer.Option("-n")] = 5,
    json: bool = False,
    dump_syms: bool = False,
):
    if build:
        build_openjdk()
    if not heap:
        heap = DEFAULT_HEAPS.get(bench)
        if not heap:
            typer.echo(f"Unknown heap size for benchmark {bench}", err=True)
            raise typer.Exit(1)
    typer.echo(f"RUN gc={gc.value} heap={heap} bench={bench}", err=True)
    java_bin = f"{PROJECT_ROOT}/openjdk/build/linux-x86_64-normal-server-release/images/jdk/bin/java"
    match gc:
        case "ix":
            gc_args = ["-XX:+UseThirdPartyHeap", "-XX:ThirdPartyHeapOptions=plan=Immix"]
        case "lxr":
            gc_args = ["-XX:+UseThirdPartyHeap", "-XX:ThirdPartyHeapOptions=plan=LXR"]
        case "g1":
            gc_args = ["-XX:+UseG1GC"]
        case "par":
            gc_args = ["-XX:+UseParallelGC"]
        case "shen":
            gc_args = ["-XX:+UseShenandoahGC"]
        case "z":
            gc_args = ["-XX:+UseZGC"]
    heap_args = [f"-Xms{heap}", f"-Xmx{heap}"]

    java_command = [java_bin, "-XX:+PreserveFramePointer", "-XX:+UnlockExperimentalVMOptions", "-XX:+UnlockDiagnosticVMOptions", "-XX:+ExitOnOutOfMemoryError", "-XX:-UseCompressedOops", *gc_args, "--add-exports", "java.base/jdk.internal.ref=ALL-UNNAMED", "-cp", "/usr/share/benchmarks/dacapo/dacapo-23.11-chopin.jar", *heap_args, "Harness", "-n", str(iter), bench]
    java_command_string = shlex.join(java_command)
    cmd = ["sudo", "bpftrace", "-B", "full", "-c", java_command_string]
    if json:
        cmd += ["-f", "json"]
    cmd += [BT_SCRIPT]
    if dump_syms:
        cmd += ["1"]
    else:
        cmd += ["0"]
    scratch = PROJECT_ROOT / "scratch"
    if scratch.exists() and scratch.is_dir():
        subprocess.check_call(["sudo", "rm", "-r", scratch])

    subprocess.check_call(cmd, cwd=PROJECT_ROOT)


if __name__ == "__main__":
    typer.run(main)
