
HOME = '/home/wenyu'
REMOTE_HOME = '/home/wenyuz' # Home path on the moma machine
JIKESRVM_ROOT = 'Projects/G1-Dev/JikesRVM' # Sub path under the local HOME
LOGS_DIR = f'{HOME}/Projects/G1-Dev/logs'
DEFAULT_MOMA_MACHINE = 'fisher'
DEFAULT_DACAPO_BENCHMARK_SUITE = 'jython'
DACAPO_VERSION = 9.12 # "9.12" # 9.12 or 2006
HEAP_SIZE = '1313M'
SINGLE_CORE = False
SINGLE_GC_THREAD = False
PAUSE_TIME_GOAL = 300
G1_GENERATIONAL = False
VERBOSE = False# or True
ENABLE_MMTK_CALLBACK = False or True
DEFAULT_BUILD_PREFIX = 'RBaseBase'

# Benchmark configs

BENCH_JVMS = [
    f'{REMOTE_HOME}/{JIKESRVM_ROOT}/dist/FastAdaptiveG1_x86_64-linux'
]