#!/usr/bin/env python3
import argparse, os
from typing import Optional

MMTK_DEV = os.path.dirname(os.path.realpath(__file__))
MMTK_OPENJDK = f'{MMTK_DEV}/mmtk-openjdk'
OPENJDK = f'{MMTK_DEV}/openjdk'
PROBES = f'{MMTK_DEV}/evaluation/probes'
DACAPO = f'/usr/share/benchmarks/dacapo/dacapo-evaluation-git-29a657f.jar'


def parse_args():
    parser = argparse.ArgumentParser(description=f'MMTk-OpenJDK Runner.\n\nExample: ./{os.path.basename(__file__)} --gc=SemiSpace --bench=xalan --heap=100M --build', add_help=False, formatter_class=argparse.RawTextHelpFormatter)
    # Required arguments
    required = parser.add_argument_group('required arguments')
    required.add_argument('--gc', type=str, required=True, help="GC plan. e.g. SemiSpace")
    required.add_argument('--bench', type=str, required=True, help="DaCapo benchmark name")
    required.add_argument('--heap', type=str, required=True, help="Heap size")
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
    optional.add_argument('--gdb', action='store_true', default=False, help="Launch GDB")
    optional.add_argument('-h', '--help', action='help', default=argparse.SUPPRESS, help='Show this help message and exit')
    return parser.parse_args()


def exec(cmd: str, cwd: str):
    print(f'🔵 {cmd}')
    result = os.system(f'cd {cwd} && {cmd}')
    if result != 0: raise RuntimeError(f'❌ {cmd}')


def config(profile: str):
    exec(f'sh configure --disable-warnings-as-errors --with-debug-level={profile} --with-target-bits=64 --with-native-debug-symbols=zipped --with-jvm-features=shenandoahgc', cwd=OPENJDK)


def build(profile: str):
    exec(f'make --no-print-directory CONF=linux-x86_64-normal-server-{profile} THIRD_PARTY_HEAP={MMTK_OPENJDK}/openjdk', cwd=OPENJDK)


def run(profile: str, gc: str, bench: str, heap: str, iter: int, noc1: bool, noc2: bool, gdb: bool, threads=Optional[int], mu=Optional[int]):
    # MMTk args
    mmtk_args = f'RUST_BACKTRACE=1 MMTK_PLAN={gc}'
    if threads is not None: mmtk_args += f' MMTK_THREADS={threads}'
    # Heap size
    heap_args = f'-XX:MetaspaceSize=1G -XX:-UseBiasedLocking -Xms{heap} -Xmx{heap} -XX:+UseThirdPartyHeap'
    # Probes args
    probe_args = f'-Dprobes=RustMMTk -Djava.library.path={PROBES} -cp {PROBES}:{PROBES}/probes.jar:{DACAPO}'
    # Compiler args
    compiler_args = ''
    if noc1 and noc2: compiler_args += '-Xint'
    elif noc1: compiler_args += '-XX:-TieredCompilation'
    elif noc2: compiler_args += 'XX:TieredStopAtLevel=3'
    # GDB Wrapper
    gdb_wrapper = 'gdb --args' if gdb else ''
    # Benchmark args
    bm_args = f''
    if mu is not None: bm_args += f' -t {mu}'
    # Run
    exec(f'{mmtk_args} {gdb_wrapper} {OPENJDK}/build/linux-x86_64-normal-server-{profile}/jdk/bin/java {heap_args} {compiler_args} {probe_args} Harness -n {iter} -c probe.DacapoChopinCallback {bench} {bm_args}', cwd=MMTK_DEV)


args = parse_args()

if args.config: config(profile=args.profile)
if args.build: build(profile=args.profile)
run(profile=args.profile, gc=args.gc, bench=args.bench, heap=args.heap, iter=args.iter, noc1=args.no_c1, noc2=args.no_c2, gdb=args.gdb, threads=args.threads, mu=args.mu)
