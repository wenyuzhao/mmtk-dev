#!/usr/bin/env python3
import argparse, os, subprocess
from typing import Optional

MMTK_DEV = os.path.dirname(os.path.realpath(__file__))
MMTK_CORE = f'{MMTK_DEV}/mmtk-core'
MMTK_JIKESRVM = f'{MMTK_DEV}/mmtk-jikesrvm'
JIKESRVM = f'{MMTK_DEV}/jikesrvm'
PROBES = f'{MMTK_DEV}/evaluation/probes'
DACAPO = f'/usr/share/benchmarks/dacapo/dacapo-evaluation-git-29a657f.jar'
BENCH_BUILDS = f'{MMTK_DEV}/evaluation/builds'


def parse_args():
    parser = argparse.ArgumentParser(description=f'MMTk-OpenJDK Runner.\n\nExample: ./{os.path.basename(__file__)} --gc=SemiSpace --bench=xalan --heap=100M --build', add_help=False, formatter_class=argparse.RawTextHelpFormatter)
    # Required arguments
    required = parser.add_argument_group('required arguments')
    required.add_argument('--gc', type=str, required=True, help="GC plan. e.g. SemiSpace")
    required.add_argument('--bench', type=str, required=True, help="DaCapo benchmark name")
    required.add_argument('--heap', type=str, required=False, help="Heap size")
    # Optional arguments
    optional = parser.add_argument_group('optional arguments')
    optional.add_argument('--profile', type=str, default='fastdebug', help="Specify build profile. Default to fastdebug")
    optional.add_argument('--release', action='store_const', const='release', dest='profile', default=False, help="Use release profile. This overrides --profile.")
    optional.add_argument('--build', action='store_true', default=False, help="Build OpenJDK")
    optional.add_argument('--config', action='store_true', default=False, help="Config OpenJDK")
    optional.add_argument('-n', '--iter', type=int, default=1, help="Number of iterations")
    optional.add_argument('--no-c1', action='store_true', default=False, help="Disable C1 compiler")
    optional.add_argument('--no-c2', action='store_true', default=False, help="Disable C2 compiler")
    optional.add_argument('--mu', type=int, nargs='?', help="Fix mutators")
    optional.add_argument('--threads', type=int, nargs='?', help="Fix GC workers")
    optional.add_argument('--features', type=str, nargs='*', help="Cargo features")
    optional.add_argument('--gdb', action='store_true', default=False, help="Launch GDB")
    optional.add_argument('--clean', action='store_true', default=False, help="`make clean` before build")
    optional.add_argument('--cp-bench', dest='build_id', type=str, nargs='?', help=f"Copy build to {BENCH_BUILDS}/jdk-mmtk-<BUILD_ID>-<commit>")
    optional.add_argument('--jdk-args', type=str, nargs='?', help="Extra OpenJDK command line arguments")
    optional.add_argument('-h', '--help', action='help', default=argparse.SUPPRESS, help='Show this help message and exit')
    return parser.parse_args()


def exec(cmd: str, cwd: str):
    print(f'🔵 {cmd}')
    result = os.system(f'cd {cwd} && {cmd}')
    if result != 0: raise RuntimeError(f'❌ {cmd}')


# def config(profile: str):
#     exec(f'sh configure --disable-warnings-as-errors --with-debug-level={profile} --with-target-bits=64 --with-native-debug-symbols=zipped --with-jvm-features=shenandoahgc', cwd=OPENJDK)


# def clean(profile: str):
#     exec(f'make clean --no-print-directory CONF=linux-x86_64-normal-server-{profile} THIRD_PARTY_HEAP={MMTK_OPENJDK}/openjdk', cwd=OPENJDK)


def build(profile: str):
    exec(f'./bin/buildit localhost {profile}--m32 --answer-yes --use-third-party-heap={MMTK_JIKESRVM} --use-third-party-build-configs={MMTK_JIKESRVM}/jikesrvm/build/configs/ --use-external-source={MMTK_JIKESRVM}/jikesrvm/rvm/src', cwd=JIKESRVM)


def run(profile: str, gc: str, bench: str, heap: str, iter: int, noc1: bool, noc2: bool, gdb: bool, threads: Optional[int], mu: Optional[int], jdk_args: Optional[str]):
    # MMTk args
    mmtk_args = f'RUST_BACKTRACE=1 MMTK_PLAN={gc}'
    if threads is not None: mmtk_args += f' MMTK_THREADS={threads}'
    # Heap size
    heap_args = f'-Xms{heap} -Xmx{heap}'
    # Probes args
    probe_args = f'-Dprobes=RustMMTk -Djava.library.path={PROBES} -cp {PROBES}:{PROBES}/probes.jar:{DACAPO}'
    # Compiler args
    compiler_args = ''
    if noc1 and noc2: compiler_args += '-Xint'
    elif noc1: compiler_args += '-XX:-TieredCompilation'
    elif noc2: compiler_args += '-XX:TieredStopAtLevel=1'
    # GDB Wrapper
    gdb_wrapper = 'gdb --args' if gdb else ''
    # Benchmark args
    bm_args = f''
    if mu is not None: bm_args += f' -t {mu}'
    # Extra
    extra_jdk_args = jdk_args if jdk_args is not None else ''
    # Run
    exec(f'{mmtk_args} {gdb_wrapper} #{JIKESRVM}/dist/{profile}_x86_64_m32-linux/rvm {heap_args} {compiler_args} {probe_args} Harness -n {iter} -c probe.DacapoChopinCallback {bench} {bm_args}', cwd=MMTK_DEV)


def bench_copy(profile: str, target: str):
    assert profile == "release", "Please use release build for benchmarking"
    commit = subprocess.check_output(['git', 'rev-parse', '--short', 'HEAD'], cwd=MMTK_CORE).decode("utf-8").strip()
    exec(f'mkdir -p {BENCH_BUILDS}', cwd=MMTK_DEV)
    exec(f'rm -rf {BENCH_BUILDS}/jdk-mmtk-{target}-{commit}', cwd=MMTK_DEV)
    exec(f'cp -r {OPENJDK}/build/linux-x86_64-normal-server-{profile} {BENCH_BUILDS}/jdk-mmtk-{target}-{commit}', cwd=MMTK_DEV)


args = parse_args()

if args.config: config(profile=args.profile)
if args.clean: clean(profile=args.profile)
if args.build: build(profile=args.profile)
run(profile=args.profile, gc=args.gc, bench=args.bench, heap=args.heap, iter=args.iter, noc1=args.no_c1, noc2=args.no_c2, gdb=args.gdb, threads=args.threads, mu=args.mu, jdk_args=args.jdk_args)
if args.build_id is not None:
    bench_copy(profile=args.profile, target=args.build_id)
