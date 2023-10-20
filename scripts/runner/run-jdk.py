#!/usr/bin/env python3

from mmtk_utils import *
from enum import Enum
import os
import subprocess
from typing import Any, Optional, List

os.environ['PERF_EVENTS'] = 'PERF_COUNT_HW_CACHE_L1D:MISS,PERF_COUNT_HW_CPU_CYCLES,PERF_COUNT_HW_INSTRUCTIONS,PERF_COUNT_HW_CACHE_DTLB:MISS'
os.environ['MMTK_PHASE_PERF_EVENTS'] = "PERF_COUNT_HW_CACHE_L1D:MISS,0,-1;PERF_COUNT_HW_CPU_CYCLES,0,-1;PERF_COUNT_HW_INSTRUCTIONS,0,-1;PERF_COUNT_HW_CACHE_DTLB:MISS,0,-1"
# os.environ['PERF_EVENTS'] = 'PERF_COUNT_HW_CACHE_DTLB:MISS'
# os.environ['MMTK_PHASE_PERF_EVENTS'] = "PERF_COUNT_HW_CACHE_DTLB:MISS,0,-1"

MMTK_OPENJDK = f"{MMTK_DEV}/mmtk-openjdk"
OPENJDK = f"{MMTK_DEV}/openjdk"


def find_dacapo():
    # Find /usr/share/benchmarks/dacapo/dacapo-23.9-RC*.chopin.jar
    for v in reversed(range(1, 10)):
        jar = f"/usr/share/benchmarks/dacapo/dacapo-23.9-RC{v}-chopin.jar"
        if os.path.isfile(jar):
            return jar
    # Find /usr/share/benchmarks/dacapo/dacapo-evaluation-git-*.jar
    DACAPO_VERSIONS = ["04132797", "6e411f33", "b00bfa9"]
    for v in DACAPO_VERSIONS:
        jar = f"/usr/share/benchmarks/dacapo/dacapo-evaluation-git-{v}.jar"
        if os.path.isfile(jar):
            return jar
    sys.exit(f"❌ Could not find a dacapo jar file")


DACAPO = find_dacapo()

HOTSPOT_GCS = {
    "G1": "-XX:+UseG1GC",
}

NO_BIASED_LOCKING = True
NO_CLASS_UNLOAD = False
NO_SOFT_REFS = False
HUGE_META_SPACE_SIZE = True
XCOMP = False


class Profile(str, Enum):
    release = "release"
    fastdebug = "fastdebug"
    slowdebug = "slowdebug"


def do_kill():
    user = os.getlogin()
    ᐅᐳᐳ(["pkill", "-f", "java", "-u", user, "-9"])


def do_config(profile: str, enable_asan: bool):
    asan_flags = ["--enable-asan"] if enable_asan else []
    ᐅᐳᐳ(
        ["sh", "configure", "--disable-zip-debug-info", "--disable-warnings-as-errors", f"--with-debug-level={profile}", "--with-target-bits=64", "--with-jvm-features=shenandoahgc", *asan_flags],
        cwd=OPENJDK,
    )
    ᐅᐳᐳ(
        ["make", "reconfigure", f"CONF=linux-x86_64-normal-server-{profile}"],
        cwd=OPENJDK,
    )


def do_clean(profile: str):
    ᐅᐳᐳ(
        ["make", "clean", f"CONF=linux-x86_64-normal-server-{profile}", f"THIRD_PARTY_HEAP={MMTK_OPENJDK}/openjdk"],
        cwd=OPENJDK,
    )


def do_build(profile: str, features: Optional[str], exploded: bool, bundle: bool, enable_asan: bool, pgo_gen: bool = False, pgo_use: bool = False):
    if exploded:
        assert not bundle, "cannot bundle an exploded image"
        target = []
    else:
        target = ["product-bundles"] if bundle else ["images"]
        ᐅᐳᐳ(
            ["rm", "-f", f"{OPENJDK}/build/linux-x86_64-normal-server-{profile}/bundles/*"],
            cwd=MMTK_DEV,
        )
    env = {}
    if features is not None:
        env["GC_FEATURES"] = features
    if pgo_gen:
        ᐅᐳᐳ([f"rm", "-rf", "/tmp/pgo-data"], cwd=MMTK_DEV)
        env["RUSTFLAGS"] = "-Cprofile-generate=/tmp/pgo-data"
    if pgo_use:
        env["RUSTFLAGS"] = "-Cprofile-use=/tmp/pgo-data/merged.profdata"
    if enable_asan:
        env["RUSTFLAGS"] = "-Zsanitizer=address"
    ᐅᐳᐳ(
        ["make", f"CONF=linux-x86_64-normal-server-{profile}", f"THIRD_PARTY_HEAP={MMTK_OPENJDK}/openjdk", *target],
        env=env,
        cwd=OPENJDK,
    )


def do_run(gc: str, bench: str, heap: str, profile: str, exploded: bool, threads: Optional[int], no_c1: bool, no_c2: bool, gdb: bool, rr: bool, mu: Optional[int], iter: int, jvm_args: Optional[List[str]], compressed_oops: bool, verbose: int = 0, enable_asan: bool = False, time_v: bool = False, jdk: Optional[str] = None):
    env = {}
    # MMTk or HotSpot GC args
    env["RUST_BACKTRACE"] = "1"
    heap_args: List[Any] = []
    if gc in HOTSPOT_GCS:
        heap_args.append(HOTSPOT_GCS[gc])
        if PROBES is not None:
            heap_args.append(f"-agentpath:{PROBES}/libperf_statistics.so")
            env["LD_PRELOAD"] = f"{PROBES}/libperf_statistics.so"
    else:
        # if PROBES is not None:
        #     heap_args.append(f"-agentpath:{PROBES}/libperf_statistics.so")
        #     env["LD_PRELOAD"] = f"{PROBES}/libperf_statistics.so"
        heap_args.append("-XX:+UseThirdPartyHeap")
        env["MMTK_PLAN"] = gc
    if threads is not None:
        env["MMTK_THREADS"] = f"{threads}"
        heap_args.append(f"-XX:ParallelGCThreads={threads}")
    if NO_SOFT_REFS:
        env["MMTK_NO_REFERENCE_TYPES"] = f"true"
        env["MMTK_NO_FINALIZER"] = f"true"
    heap_args += [f"-Xms{heap}", f"-Xmx{heap}"]
    if HUGE_META_SPACE_SIZE or NO_CLASS_UNLOAD:
        heap_args.append("-XX:MetaspaceSize=1G")
    # Probes args
    probe_args: List[Any] = []
    callback_args: List[Any] = []
    if PROBES is not None:
        probe_args += ["--add-exports", "java.base/jdk.internal.ref=ALL-UNNAMED", "-Dprobes=RustMMTk", f"-Djava.library.path={PROBES}", "-cp", f"{PROBES}:{PROBES}/probes.jar:{DACAPO}"]
        callback_args += ["-c", "probe.DacapoChopinCallback"]
    else:
        probe_args += ["--add-exports", "java.base/jdk.internal.ref=ALL-UNNAMED", "-cp", DACAPO]
    # Compiler args
    compiler_args: List[Any] = []
    if no_c1 and no_c2:
        compiler_args.append("-Xint")
    elif no_c1:
        compiler_args.append("-XX:-TieredCompilation")
    elif no_c2:
        compiler_args.append("-XX:TieredStopAtLevel=1")
    # GDB Wrapper
    debugger_wrapper: List[Any] = []
    if gdb:
        debugger_wrapper += ["rust-gdb", "--args"]
    elif rr:
        debugger_wrapper += ["rr", "record"]
    # Benchmark args
    bm_args: List[Any] = []
    if mu is not None:
        bm_args += ["-t", f"{mu}"]
    # Extra
    extra_jvm_args = jvm_args or []
    extra_jvm_args += ["-XX:+UnlockExperimentalVMOptions", "-XX:+UnlockDiagnosticVMOptions", "-XX:+ExitOnOutOfMemoryError"]
    if NO_BIASED_LOCKING:
        extra_jvm_args.append("-XX:-UseBiasedLocking")
    if NO_CLASS_UNLOAD:
        extra_jvm_args += ["-XX:-ClassUnloading", "-XX:-ClassUnloadingWithConcurrentMark"]
    if XCOMP:
        extra_jvm_args.append("-Xcomp")
    if not compressed_oops:
        extra_jvm_args += ["-XX:-UseCompressedOops", "-XX:-UseCompressedClassPointers"]
    if enable_asan:
        env["ASAN_OPTIONS"] = "handle_segv=0"
    if verbose != 0:
        env["MMTK_VERBOSE"] = f"{verbose}"
        if verbose >= 3:
            extra_jvm_args += ["-Xlog:gc*,gc+phases=debug"]
        elif verbose >= 2:
            extra_jvm_args += ["-Xlog:gc"]
    time_v_wrapper = ["/bin/time", "-v"] if time_v else []
    # Run
    jdk_build_dir = f"{OPENJDK}/build/linux-x86_64-normal-server-{str(profile)}"
    java = f"{jdk_build_dir}/jdk/bin/java" if exploded else f"{jdk_build_dir}/images/jdk/bin/java"
    if jdk is not None:
        java = f"{jdk}/bin/java"
    ᐅᐳᐳ(
        [*debugger_wrapper, *time_v_wrapper, java, *extra_jvm_args, *heap_args, *compiler_args, *probe_args, "Harness", "-n", f"{iter}", *callback_args, bench, *bm_args],
        cwd=MMTK_DEV,
        env=env,
    )


def do_cp_bench(profile: str, target: str, no_commit_hash: bool):
    assert profile == "release", "Please use release build for benchmarking"
    # Get mmtk-core commit hash
    commit = subprocess.check_output(["git", "rev-parse", "--short", "HEAD"], cwd=MMTK_CORE).decode("utf-8").strip()
    name = f"{target}" if no_commit_hash else f"{target}-{commit}"
    ᐅᐳᐳ(["mkdir", "-p", BENCH_BUILDS], cwd=MMTK_DEV)
    # Get bundle file
    bundle = (
        subprocess.check_output(
            ["bash", "-c", f"ls {OPENJDK}/build/linux-x86_64-normal-server-{profile}/bundles/*.tar.gz | grep -v -e symbols -e demos"],
            cwd=MMTK_DEV,
        )
        .decode("utf-8")
        .strip()
    )
    # Delete previous builds
    ᐅᐳᐳ(["rm", "-rf", f"{BENCH_BUILDS}/{name}"], cwd=MMTK_DEV)
    ᐅᐳᐳ(["rm", "-f", f"{BENCH_BUILDS}/{name}.tar.gz"], cwd=MMTK_DEV)
    # Copy bundle file
    ᐅᐳᐳ(["cp", bundle, f"{BENCH_BUILDS}/{name}.tar.gz"], cwd=MMTK_DEV)
    # Extract and remove bundle file
    ᐅᐳᐳ(["mkdir", "-p", f"{BENCH_BUILDS}/{name}"], cwd=MMTK_DEV)
    ᐅᐳᐳ(["tar", "-xf", f"{BENCH_BUILDS}/{name}.tar.gz", "-C", f"{BENCH_BUILDS}/{name}"], cwd=MMTK_DEV)
    ᐅᐳᐳ(["rm", f"{BENCH_BUILDS}/{name}.tar.gz"], cwd=MMTK_DEV)


@app.command()
def main(
    gc: str = option(..., help="GC plan. e.g. SemiSpace"),
    heap: str = option(..., help="Heap size"),
    bench: str = option(..., help="DaCapo benchmark name"),
    # Optional build and run args
    profile: Profile = option(Profile.fastdebug, help="Specify build profile. Default to fastdebug"),
    release: bool = option(False, "--release", "-r", help="Overwrite --profile and force release build"),
    exploded: bool = option(False, "--exploded", "-x", help="Build or run the exploded image"),
    # Optional build args
    build: bool = option(False, "--build", "-b", help="Build OpenJDK"),
    config: bool = option(False, "--config", help="Config OpenJDK"),
    features: Optional[str] = option(None, help="Cargo features"),
    pgo: bool = option(False, "--pgo", help="Profile-guided Optimization"),
    cp_bench: Optional[str] = option(None, help=f"Copy build to mmtk-dev/evaluation/builds/<cp_bench>-<commit>"),
    cp_bench_no_commit_hash: bool = option(False, "--cp-bench-no-commit-hash", help=f"Don't put commit hash as part of the build folder name"),
    # Optional run args
    iter: int = option(1, "--iter", "-n", help="Number of iterations"),
    no_c1: bool = option(False, "--no-c1", help="Disable C1 compiler"),
    no_c2: bool = option(False, "--no-c2", help="Disable C2 compiler"),
    mu: Optional[int] = option(None, help="Fix number of mutators"),
    threads: Optional[int] = option(None, help="Fix number of GC workers"),
    gdb: bool = option(False, "--gdb", help="Launch with GDB"),
    rr: bool = option(False, "--rr", help="Launch with rr record"),
    clean: bool = option(False, "--clean", help="`make clean` before build"),
    kill: bool = option(False, "--kill", help="Kill all existing java processes"),
    jdk: Optional[str] = option(None, help=f"Use a different pre-built JDK"),
    jvm_args: Optional[List[str]] = option(None, help=f"Extra OpenJDK command line arguments"),
    compressed_oops: bool = option(True, help=f"UseCompressedOops"),
    verbose: int = option(0, "--verbose", "-v", help=f"mmtk verbosity"),
    no_run: bool = option(False, "--no-run", help=f"Don't run any java program"),
    enable_asan: bool = option(False, "--enable-asan", help=f"Enable address sanitizer"),
    time_v: bool = option(False, "--time-v", help=f"/bin/time -v wrapper"),
):
    """
    Example: ./run-jdk --gc=SemiSpace --bench=lusearch --heap=500M --exploded --profile=release -n 5 --build
    """
    if release:
        profile = Profile.release
    profile_v = str(profile.value)
    if kill:
        do_kill()
    if config:
        do_config(profile=profile_v, enable_asan=enable_asan)
    if clean:
        do_clean(profile=profile_v)
    if build:
        assert jdk is None
        if pgo:
            assert profile_v == "release"
            assert not enable_asan
            do_build(profile=profile_v, features=features, exploded=exploded, bundle=cp_bench is not None, enable_asan=False, pgo_gen=True)

            def run_with_pgo(bench: str, heap: str):
                do_run(gc=gc, bench=bench, heap=heap, profile=profile_v, exploded=exploded, threads=threads, no_c1=no_c1, no_c2=no_c2, gdb=gdb, rr=rr, mu=mu, iter=iter, jvm_args=jvm_args, compressed_oops=compressed_oops)

            run_with_pgo(bench="lusearch", heap="200M")
            run_with_pgo(bench="h2", heap="3000M")
            run_with_pgo(bench="cassandra", heap="800M")
            run_with_pgo(bench="tomcat", heap="300M")
            ᐅᐳᐳ(["./scripts/llvm-profdata", "merge", "-o", "/tmp/pgo-data/merged.profdata", "/tmp/pgo-data"])
        do_build(profile=profile_v, features=features, exploded=exploded, bundle=cp_bench is not None, enable_asan=enable_asan, pgo_use=pgo)
    if not no_run:
        do_run(gc=gc, bench=bench, heap=heap, profile=profile_v, exploded=exploded, threads=threads, no_c1=no_c1, no_c2=no_c2, gdb=gdb, rr=rr, mu=mu, iter=iter, jvm_args=jvm_args, compressed_oops=compressed_oops, verbose=verbose, enable_asan=enable_asan, time_v=time_v, jdk=jdk)
    if cp_bench is not None:
        do_cp_bench(profile=profile_v, target=cp_bench, no_commit_hash=cp_bench_no_commit_hash)


if __name__ == "__main__":
    app(prog_name="run-jdk")
