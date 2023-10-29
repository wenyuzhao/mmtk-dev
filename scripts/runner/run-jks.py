#!/usr/bin/env python3

from mmtk_utils import *
from enum import Enum
import os
import subprocess
from typing import Any, Optional, List

MMTK_JIKESRVM = f"{MMTK_DEV}/mmtk-jikesrvm"
JIKESRVM = f"{MMTK_DEV}/jikesrvm"
DACAPO = "/usr/share/benchmarks/dacapo/dacapo-9.12-bach.jar"

class Profile(str, Enum):
    release = "release"
    fastdebug = "fastdebug"
    slowdebug = "slowdebug"


def do_kill():
    user = os.getlogin()
    ᐅᐳᐳ(["pkill", "-f", "rvm", "-u", user, "-9"])


def do_build(target: str):
    env = {}
    ᐅᐳᐳ(
        ["./bin/buildit", "localhost", target, "--use-third-party-heap=../mmtk-jikesrvm", "--use-third-party-build-configs=../mmtk-jikesrvm/jikesrvm/build/configs/", "--use-external-source=../mmtk-jikesrvm/jikesrvm/rvm/src", "--m32", "--answer-yes"],
        env=env,
        cwd=JIKESRVM,
    )


def do_run(target: str, bench: str, heap: str, iter: str):
    env = {}
    # MMTk or HotSpot GC args
    env["RUST_BACKTRACE"] = "1"
    env["LD_LIBRARY_PATH"] = f"dist/{target}_x86_64_m32-linux/"

    heap_args: List[Any] = [ f"-Xms{heap}", f"-Xmx{heap}" ]
    dacapo_args = [ "-jar", "/usr/share/benchmarks/dacapo/dacapo-9.12-bach.jar", bench, "-n", f"{iter}" ]

    ᐅᐳᐳ(
        [f"dist/{target}_x86_64_m32-linux/rvm", *heap_args, *dacapo_args],
        env=env,
        cwd=JIKESRVM,
    )

@app.command()
def main(
    target: str = option(..., help="Target with GC plan. e.g. RBaseBaseSemiSpace"),
    heap: str = option(..., help="Heap size"),
    bench: str = option(..., help="DaCapo benchmark name"),
    # Optional run args
    iter: int = option(1, "--iter", "-n", help="Number of iterations"),
    build: bool = option(False, "--build", "-b", help="Build JikesRVM"),
    no_run: bool = option(False, "--no-run", help=f"Don't run any java program"),
):
    """
    Example: ./run-jks --target=RBaseBaseSemiSpace --bench=lusearch --heap=100M -n 5 --build
    """
    if build:
        do_build(target=target)
    if not no_run:
        do_run(target=target, bench=bench, heap=heap, iter=iter)

if __name__ == "__main__":
    app(prog_name="run-jks")
