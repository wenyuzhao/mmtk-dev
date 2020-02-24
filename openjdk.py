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
RUST_PROFILE = 'release' if DEBUG_LEVEL == 'release' else 'debug'
ENV = f'RUST_BACKTRACE=1 LD_LIBRARY_PATH=$LD_LIBRARY_PATH:{OPENJDK}/mmtk/target/{RUST_PROFILE}'
JAVA = f'{OPENJDK}/build/linux-x86_64-normal-server-{DEBUG_LEVEL}/jdk/bin/java'



@task.register
def build(gc=DEFAULT_GC, config=False):
    if config:
        task.exec(f'bash configure --disable-warnings-as-errors --with-debug-level={DEBUG_LEVEL}', cwd=OPENJDK)
    release_flag = '--release' if DEBUG_LEVEL == 'release' else ''
    task.exec(f'cargo +nightly build --no-default-features --features openjdk,{gc} {release_flag}', cwd=f'{OPENJDK}/mmtk')
    task.exec(f'CONF=linux-x86_64-normal-server-{DEBUG_LEVEL} make', cwd=OPENJDK)

@task.register
def run(gc=DEFAULT_GC, threads=None, n=None, no_mmtk=False):
    heap = f'-Xms{HEAP} -Xmx{HEAP}'
    bm_classpath, bm_entry = dacapo.get_config(BENCH_SUITE, BENCH, probes=False)
    if no_mmtk:
        command = f'{ENV} {JAVA} -XX:-UseCompressedOops {heap} -server -cp {bm_classpath} {bm_entry}'
    else:
        command = f'{ENV} {JAVA} -XX:+UseMMTk -XX:-UseCompressedOops {heap} -server -cp {bm_classpath} {bm_entry}'
    task.exec(command, machine=MACHINE, cwd=task.LOG_DIR)


assert MACHINE == 'localhost'
task.run()
