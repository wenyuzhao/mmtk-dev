#!/usr/bin/env python3
import task_runner as task
import dacapo
import os

# Build/Run Config
HEAP = '500M'
DEFAULT_GC = 'semispace'
BENCH = 'lusearch'
BENCH_SUITE = 'dacapo-9.12'
DEBUG_LEVEL = 'slowdebug' # release, fastdebug, slowdebug, optimized

# Project Config
MACHINE = 'localhost'
OPENJDK = '~/mmtk-openjdk/repos/openjdk'
ENV = f'RUST_BACKTRACE=1 LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/home/wenyuz/'
JAVA = f'{OPENJDK}/build/linux-x86_64-normal-server-{DEBUG_LEVEL}/jdk/bin/java'



@task.register
def build(gc=DEFAULT_GC, config=False, nommtk=False):
    if config:
        task.exec(f'sh configure --disable-warnings-as-errors --with-debug-level={DEBUG_LEVEL}', cwd=OPENJDK)
    if nommtk:
        command = f'{ENV} make CONF=linux-x86_64-normal-server-{DEBUG_LEVEL}'
    else:
        command = f'{ENV} make CONF=linux-x86_64-normal-server-{DEBUG_LEVEL} THIRD_PARTY_HEAP=$PWD/../../openjdk'
    task.exec(command, cwd=OPENJDK)

@task.register
def clean(gc=DEFAULT_GC):
    task.exec(f'{ENV} make clean CONF=linux-x86_64-normal-server-{DEBUG_LEVEL}', cwd=OPENJDK)


@task.register
def tests():
    task.exec('javac *.java', machine=MACHINE, cwd=task.DEV_DIR + '/tests')

@task.register
def run(gc=DEFAULT_GC, threads=None, n=None, mmtk=True, log=False, jclass=None, dump=None, intonly=False, c1only=False, c2only=False):
    # Heap option
    heap = f'-Xms{HEAP} -Xmx{HEAP}'
    # ASM Dump option
    dumpoption = f'"-XX:CompileCommand=print,*{dump}" -XX:-TieredCompilation -XX:CompileOnly={dump}' if dump is not None else ''
    # JIT Option
    if intonly:
        assert not c1only and not c2only
        jitoption = '-Xint'
    elif c1only:
        assert not intonly and not c2only
        jitoption = '-XX:TieredStopAtLevel=1'
    elif c2only:
        assert not intonly and not c1only
        jitoption = '-XX:-TieredCompilation'
    else:
        jitoption = ''
    # GC Option
    if not mmtk:
        gcoption = f'-XX:-UseCompressedOops -XX:-UseTLAB -XX:+UseG1GC'
    else:
        gcoption = f'-XX:-UseCompressedOops -XX:+UseThirdPartyHeap'
    # Benchmark entry
    if jclass is not None:
        tests()
        bm_classpath, bm_entry = '../', jclass
    else:
        bm_classpath, bm_entry = dacapo.get_config(BENCH_SUITE, BENCH, probes=False)

    command = f'{ENV} {JAVA} {gcoption} {heap} {dumpoption} {jitoption} -server -cp {bm_classpath} {bm_entry}'

    print(command, log)
    log = f'{task.LOG_DIR}/openjdk.log' if log else None
    task.exec(command, machine=MACHINE, cwd=task.LOG_DIR, stdout=log)


assert MACHINE == 'localhost'
task.run()


# ./openjdk.py run --jclass=tests/Main --dump=tests/Main.writeFieldOnce --log