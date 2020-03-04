#!/usr/bin/env python3
import task_runner as task
import dacapo
import os

# Build/Run Config
HEAP = '512M'
DEFAULT_GC = 'semispace'
BENCH = 'lusearch'
BENCH_SUITE = 'dacapo-9.12'
DEBUG_LEVEL = 'release' # release, fastdebug, slowdebug, optimized

# Project Config
MACHINE = 'localhost'
OPENJDK = '~/OpenJDK-Rust'
ENV = f'RUST_BACKTRACE=1'
JAVA = f'{OPENJDK}/build/linux-x86_64-normal-server-{DEBUG_LEVEL}/jdk/bin/java'



@task.register
def build(gc=DEFAULT_GC, config=False):
    if config:
        task.exec(f'sh configure --disable-warnings-as-errors --with-debug-level={DEBUG_LEVEL}', cwd=OPENJDK)
    task.exec(f'{ENV} make CONF=linux-x86_64-normal-server-{DEBUG_LEVEL}', cwd=OPENJDK)

@task.register
def run(gc=DEFAULT_GC, threads=None, n=None, no_mmtk=False, log=False):
    heap = f'-Xms{HEAP} -Xmx{HEAP}'
    bm_classpath, bm_entry = dacapo.get_config(BENCH_SUITE, BENCH, probes=False)
    if no_mmtk:
        command = f'{ENV} {JAVA} -XX:-UseCompressedOops {heap} -server -cp {bm_classpath} {bm_entry}'
    else:
        command = f'{ENV} {JAVA} -XX:+UseMMTk -XX:-UseCompressedOops -XX:-UseCompressedClassPointers {heap} -server -cp {bm_classpath} {bm_entry}'
    log = f'{task.LOG_DIR}/openjdk.log' if log else None
    task.exec(command, machine=MACHINE, cwd=task.LOG_DIR, stdout=log)


assert MACHINE == 'localhost'
task.run()
