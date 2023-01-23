#!/usr/bin/env python3
import argparse
import os
import subprocess
from typing import Optional, Tuple
from dataclasses import dataclass


MMTK_DEV = os.path.dirname(os.path.realpath(__file__))
MMTK_CORE = f'{MMTK_DEV}/mmtk-core'
MMTK_OPENJDK = f'{MMTK_DEV}/mmtk-openjdk'
OPENJDK = f'{MMTK_DEV}/openjdk'
PROBES = f'{MMTK_DEV}/evaluation/probes'
# DACAPO = f'/usr/share/benchmarks/dacapo/dacapo-evaluation-git-f480064.jar'
DACAPO = '/usr/share/benchmarks/dacapo/dacapo-evaluation-git-6e411f33.jar'
BENCH_BUILDS = f'{MMTK_DEV}/evaluation/builds'

# HOTSPOT_GCS = ['G1', 'Shen', 'Shenandoah', 'Z', 'ZGC', 'Parallel', 'Serial']
HOTSPOT_GCS = {
    'G1': '-XX:+UseG1GC',
}

NO_BIASED_LOCKING = True
NO_CLASS_UNLOAD = False
HUGE_META_SPACE_SIZE = False
XCOMP = False


@dataclass
class BuildArgs:
    profile: str
    exploded: bool
    bundle: bool
    features: Optional[str]
    build_id: Optional[str]


@dataclass
class RunArgs:
    gc: str
    bench: str
    heap: Optional[str]
    iter: int
    noc1: bool
    noc2: bool
    gdb: bool
    rr: bool
    exploded: bool
    threads: Optional[int]
    mu: Optional[int]
    jdk_args: Optional[str]
    compressed_oops: bool


@dataclass
class Commands:
    kill: bool
    config: bool
    clean: bool
    build: bool
    run: bool
    cp_bench: bool


def parse_args() -> Tuple[Commands, BuildArgs, RunArgs]:
    parser = argparse.ArgumentParser(
        description=f'MMTk-OpenJDK Runner.\n\nExample: ./{os.path.basename(__file__)} --gc=SemiSpace --bench=xalan --heap=100M --build', add_help=False, formatter_class=argparse.RawTextHelpFormatter)
    # Required arguments
    required = parser.add_argument_group('required arguments')
    required.add_argument('--gc', type=str, required=True,
                          help="GC plan. e.g. SemiSpace")
    required.add_argument('--bench', type=str, required=True,
                          help="DaCapo benchmark name")
    # Optional arguments
    required.add_argument('--heap', type=str, help="Heap size")
    optional = parser.add_argument_group('optional arguments')
    optional.add_argument('--profile', type=str, default='fastdebug',
                          help="Specify build profile. Default to fastdebug")
    optional.add_argument('--release', action='store_const', const='release', dest='profile',
                          default=False, help="Use release profile. This overrides --profile.")
    optional.add_argument('--build', action='store_true',
                          default=False, help="Build OpenJDK")
    optional.add_argument('--config', action='store_true',
                          default=False, help="Config OpenJDK")
    optional.add_argument('-n', '--iter', type=int,
                          default=1, help="Number of iterations")
    optional.add_argument('--no-c1', action='store_true',
                          default=False, help="Disable C1 compiler")
    optional.add_argument('--no-c2', action='store_true',
                          default=False, help="Disable C2 compiler")
    optional.add_argument('--mu', type=int, nargs='?', help="Fix mutators")
    optional.add_argument('--threads', type=int,
                          nargs='?', help="Fix GC workers")
    optional.add_argument('--features', type=str,
                          nargs='*', help="Cargo features")
    optional.add_argument('--gdb', action='store_true',
                          default=False, help="Launch with GDB")
    optional.add_argument('--rr', action='store_true',
                          default=False, help="Launch with rr record")
    optional.add_argument('--clean', action='store_true',
                          default=False, help="`make clean` before build")
    optional.add_argument('--exploded', action='store_true',
                          default=False, help="Build exploded image")
    optional.add_argument('--kill', action='store_true', default=False,
                          help=f"Kill all existing Java and {os.path.basename(__file__)} processes")
    optional.add_argument('--cp-bench', dest='build_id', type=str, nargs='?',
                          help=f"Copy build to {BENCH_BUILDS}/jdk-mmtk-<BUILD_ID>-<commit>")
    optional.add_argument('--jdk-args', type=str, nargs='?',
                          help="Extra OpenJDK command line arguments")
    optional.add_argument('--compressed-oops', action='store_true',
                          default=False, help="UseCompressedOops")
    optional.add_argument('-h', '--help', action='help',
                          default=argparse.SUPPRESS, help='Show this help message and exit')
    # parse
    args = parser.parse_args()
    commands = Commands(
        kill=args.kill,
        config=args.config,
        clean=args.clean,
        build=args.build,
        run=True,
        cp_bench=args.build_id is not None,
    )
    build_args = BuildArgs(profile=args.profile, exploded=args.exploded,
                           bundle=args.build_id is not None, features=args.features, build_id=args.build_id)
    run_args = RunArgs(gc=args.gc, bench=args.bench, heap=args.heap, iter=args.iter, noc1=args.no_c1, noc2=args.no_c2, gdb=args.gdb,
                       rr=args.rr, exploded=args.exploded, threads=args.threads, mu=args.mu, jdk_args=args.jdk_args, compressed_oops=args.compressed_oops)
    return (commands, build_args, run_args)


def exec(cmd: str, cwd: str = MMTK_DEV):
    print(f'🔵 {cmd}')
    result = os.system(f'cd {cwd} && {cmd}')
    if result != 0:
        raise RuntimeError(f'❌ {cmd}')


def config(profile: str):
    exec(
        f'sh configure --disable-zip-debug-info --disable-warnings-as-errors --with-debug-level={profile} --with-target-bits=64 --with-jvm-features=shenandoahgc', cwd=OPENJDK)
    exec(
        f'make reconfigure CONF=linux-x86_64-normal-server-{profile}', cwd=OPENJDK)


def clean(profile: str):
    exec(
        f'make clean --no-print-directory CONF=linux-x86_64-normal-server-{profile} THIRD_PARTY_HEAP={MMTK_OPENJDK}/openjdk', cwd=OPENJDK)


def build(build_args: BuildArgs):
    if build_args.exploded:
        assert not build_args.bundle, "cannot bundle an exploded image"
        target = ''
    else:
        target = 'product-bundles' if build_args.bundle else 'images'
        exec(
            f'rm -f {OPENJDK}/build/linux-x86_64-normal-server-{build_args.profile}/bundles/*', cwd=MMTK_DEV)
    features = f'GC_FEATURES={",".join(build_args.features)} 'if build_args.features is not None else ''
    exec(
        f'make --no-print-directory CONF=linux-x86_64-normal-server-{build_args.profile} THIRD_PARTY_HEAP={MMTK_OPENJDK}/openjdk {target} {features}', cwd=OPENJDK)


def run(build_args: BuildArgs, run_args: RunArgs):
    # MMTk or HotSpot GC args
    mmtk_env_args = 'RUST_BACKTRACE=1'
    if run_args.gc in HOTSPOT_GCS:
        hs_gc = HOTSPOT_GCS[run_args.gc]
        if PROBES is not None:
            hs_gc += f' -agentpath:{PROBES}/libperf_statistics.so'
            mmtk_env_args += f' LD_PRELOAD={PROBES}/libperf_statistics.so'
    else:
        hs_gc = '-XX:+UseThirdPartyHeap'
        mmtk_env_args += f' MMTK_PLAN={run_args.gc}'
    if run_args.threads is not None:
        mmtk_env_args += f' MMTK_THREADS={run_args.threads}'
    # Heap size
    heap_size = f'-Xms{run_args.heap} -Xmx{run_args.heap}' if run_args.heap is not None else ''
    heap_args = f'{heap_size}'
    if HUGE_META_SPACE_SIZE or NO_CLASS_UNLOAD:
        heap_args += ' -XX:MetaspaceSize=1G'
    # Probes args
    if PROBES is not None:
        probe_args = f'--add-exports java.base/jdk.internal.ref=ALL-UNNAMED -Dprobes=RustMMTk -Djava.library.path={PROBES} -cp {PROBES}:{PROBES}/probes.jar:{DACAPO}'
        callback_args = '-c probe.DacapoChopinCallback'
    else:
        probe_args = f'--add-exports java.base/jdk.internal.ref=ALL-UNNAMED -cp {DACAPO}'
        callback_args = ''
    # Compiler args
    compiler_args = ''
    if run_args.noc1 and run_args.noc2:
        compiler_args += '-Xint'
    elif run_args.noc1:
        compiler_args += '-XX:-TieredCompilation'
    elif run_args.noc2:
        compiler_args += '-XX:TieredStopAtLevel=1'
    # GDB Wrapper
    if run_args.gdb:
        debugger_wrapper = 'gdb --args'
    elif run_args.rr:
        debugger_wrapper = 'rr record'
    else:
        debugger_wrapper = ''
    # Benchmark args
    bm_args = ''
    if run_args.mu is not None:
        bm_args += f' -t {run_args.mu}'
    # Extra
    extra_jdk_args = run_args.jdk_args if run_args.jdk_args is not None else ''
    extra_jdk_args += ' -XX:+UnlockExperimentalVMOptions -XX:+UnlockDiagnosticVMOptions -XX:-InlineObjectCopy'
    if NO_BIASED_LOCKING:
        extra_jdk_args += ' -XX:-UseBiasedLocking'
    if NO_CLASS_UNLOAD:
        extra_jdk_args += ' -XX:-ClassUnloading -XX:-ClassUnloadingWithConcurrentMark'
    if XCOMP:
        extra_jdk_args += ' -Xcomp'
    if not run_args.compressed_oops:
        extra_jdk_args += ' -XX:-UseCompressedOops -XX:-UseCompressedClassPointers'
    # Run
    java = f'{OPENJDK}/build/linux-x86_64-normal-server-{build_args.profile}/jdk/bin/java' if build_args.exploded else f'{OPENJDK}/build/linux-x86_64-normal-server-{build_args.profile}/images/jdk/bin/java'
    exec(f'{mmtk_env_args} {debugger_wrapper} {java} {extra_jdk_args} {hs_gc} {heap_args} {compiler_args} {probe_args} Harness -n {run_args.iter} {callback_args} {run_args.bench} {bm_args}', cwd=MMTK_DEV)


def bench_copy(profile: str, target: str):
    assert profile == "release", "Please use release build for benchmarking"
    # Get mmtk-core commit hash
    commit = subprocess.check_output(
        ['git', 'rev-parse', '--short', 'HEAD'], cwd=MMTK_CORE).decode("utf-8").strip()
    exec(f'mkdir -p {BENCH_BUILDS}', cwd=MMTK_DEV)
    # Get bundle file
    bundle = subprocess.check_output(
        ['bash', '-c', f'ls {OPENJDK}/build/linux-x86_64-normal-server-{profile}/bundles/*.tar.gz | grep -v -e symbols -e demos'], cwd=MMTK_DEV).decode("utf-8").strip()
    # Delete previous builds
    exec(f'rm -rf {BENCH_BUILDS}/jdk-mmtk-{target}-{commit}', cwd=MMTK_DEV)
    exec(f'rm -f {BENCH_BUILDS}/jdk-mmtk-{target}-{commit}.tar.gz', cwd=MMTK_DEV)
    # Copy bundle file
    exec(f'cp {bundle} {BENCH_BUILDS}/jdk-mmtk-{target}-{commit}.tar.gz', cwd=MMTK_DEV)
    # Extract and remove bundle file
    exec(f'mkdir -p {BENCH_BUILDS}/jdk-mmtk-{target}-{commit}', cwd=MMTK_DEV)
    exec(f'tar -xf {BENCH_BUILDS}/jdk-mmtk-{target}-{commit}.tar.gz -C {BENCH_BUILDS}/jdk-mmtk-{target}-{commit}', cwd=MMTK_DEV)
    exec(f'rm {BENCH_BUILDS}/jdk-mmtk-{target}-{commit}.tar.gz', cwd=MMTK_DEV)


def kill():
    user = os.getlogin()
    os.system(f'pkill -f java -u {user} -9')


def main():
    commands, build_args, run_args = parse_args()

    if commands.kill:
        kill()
    if commands.config:
        config(profile=build_args.profile)
    if commands.clean:
        clean(profile=build_args.profile)
    if commands.build:
        build(build_args)
    if commands.run:
        run(build_args, run_args)
    if commands.cp_bench:
        assert build_args.build_id is not None
        bench_copy(profile=build_args.profile, target=build_args.build_id)


main()
