import os
from pathlib import Path

RUST_MMTK = False

# Project & Build Configs

HOME = '/home/wenyu'
REMOTE_HOME = '/home/wenyuz' # Home path on the moma machine
JIKESRVM_ROOT = 'Projects/JikesRVM-G1' if not RUST_MMTK else 'Projects/JikesRVM-Rust' # Sub path under the local HOME
OPENJDK_ROOT = 'Projects/OpenJDK-MMTk'

# Runtime Configs

DEFAULT_DACAPO_BENCHMARK_SUITE = 'lusearch'
DACAPO_VERSION = 9.12 # 9.12 or 2006
HEAP_SIZE = 100 # mb
SINGLE_CORE = False
SINGLE_GC_THREAD = True 
PAUSE_TIME_GOAL = 20 # ms
G1_GENERATIONAL = False
VERBOSE = False# or True
ENABLE_MMTK_CALLBACK = False# or True
LATENCY_TIMER = False

# Moma Machine Configs

DEFAULT_MOMA_MACHINE = 'fisher'

# Benchmark Configs

RUN_CONFIG = 'RunConfig-G1.pm'
HEAP_ARGS = '8 5' #'8 1 3 5 7'
BENCH_JVMS = [
    # 'FastAdaptiveRegional',
    # 'FastAdaptiveLSRegional',
    # 'FastAdaptiveConcRegional',
    # 'FastAdaptiveG1',
    # 'FastAdaptiveG10064K',
    # 'FastAdaptiveG10128K',
    # 'FastAdaptiveG10256K',
    # 'FastAdaptiveG10512K',
    # 'FastAdaptiveG11024K',
    # 'FastAdaptiveG1NoBarrier',
    # 'FastAdaptiveG1SATBCond',
    # 'FastAdaptiveG1SATBUncond',
    # 'FastAdaptiveG1RemSetBarrier',
    # 'FastAdaptiveG1AllBarriers',
    'FastAdaptiveRegional',
    'FastAdaptiveSemiSpace',
]
BENCH_JVMS = [ f'{REMOTE_HOME}/{JIKESRVM_ROOT}/dist/{x}_x86_64-linux' for x in BENCH_JVMS ]

# Derived Configs

DEV_ROOT = Path(os.path.dirname(os.path.realpath(__file__))).parent
DEFAULT_BUILD_PREFIX = 'RBaseBase' if RUST_MMTK else 'BaseBase'
LOGS_DIR = f'{DEV_ROOT}/logs'
