#!/usr/bin/env python3
import task_runner as task
import dacapo
import os

# Build/Run Config
HEAP = '512M'
DEFAULT_GC = 'semispace'
BENCH = 'lusearch'
BENCH_SUITE = 'dacapo-9.12'
DEBUG_LEVEL = 'slowdebug' # release, fastdebug, slowdebug, optimized

# Project Config
MACHINE = 'localhost'
OPENJDK = '~/mmtk-openjdk/repos/openjdk'
ENV = f'RUST_BACKTRACE=1'
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
def run(gc=DEFAULT_GC, threads=None, n=None, nommtk=False, log=False, jclass=None, dump=None):
    heap = f'-Xms{HEAP} -Xmx{HEAP}'
    
    compilecommand = f'-XX:CompileCommand=print,*{dump}' if dump is not None else ''

    if jclass is not None:
        tests()
        bm_classpath, bm_entry = '../', jclass
    else:
        bm_classpath, bm_entry = dacapo.get_config(BENCH_SUITE, BENCH, probes=False)

    if nommtk:
        command = f'{ENV} {JAVA} -XX:-UseCompressedOops -XX:-UseTLAB -XX:+UseG1GC {heap} -server -cp {bm_classpath} {bm_entry}'
    else:
        command = f'{ENV} {JAVA} -XX:+UseThirdPartyHeap -XX:-UseCompressedOops {heap} {compilecommand} -server -cp {bm_classpath} {bm_entry}'

    print(command)
    log = f'{task.LOG_DIR}/openjdk.log' if log else None
    task.exec(command, machine=MACHINE, cwd=task.LOG_DIR, stdout=log)


assert MACHINE == 'localhost'
task.run()
