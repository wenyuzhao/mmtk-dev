import os
from pathlib import Path



# Project & Build Configs

HOME = '/home/wenyu'
REMOTE_HOME = '/home/wenyuz' # Home path on the moma machine
JIKESRVM_ROOT = 'Projects/G1-Dev/JikesRVM' # Sub path under the local HOME
RUST_MMTK_SUPPORT = False

# Runtime Configs

DEFAULT_DACAPO_BENCHMARK_SUITE = 'avrora'
DACAPO_VERSION = 9.12 # 9.12 or 2006
HEAP_SIZE = 537 # mb
SINGLE_CORE = False
SINGLE_GC_THREAD = False
PAUSE_TIME_GOAL = 300 # ms
G1_GENERATIONAL = False
VERBOSE = False# or True
ENABLE_MMTK_CALLBACK = False or True

# Moma Machine Configs

DEFAULT_MOMA_MACHINE = 'fisher'

# Benchmark Configs

RUN_CONFIG = 'RunConfig-FootprintRegionSize.pm'
HEAP_ARGS = '8 7'
BENCH_JVMS = [
    f'{REMOTE_HOME}/{JIKESRVM_ROOT}/dist/FastAdaptiveG1_x86_64-linux'
]

# Derived Configs

DEV_ROOT = Path(os.path.dirname(os.path.realpath(__file__))).parent
DEFAULT_BUILD_PREFIX = 'RBaseBase' if RUST_MMTK_SUPPORT else 'BaseBase'
LOGS_DIR = f'{DEV_ROOT}/logs'
