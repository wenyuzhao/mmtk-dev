#!/usr/bin/env python3
import task_runner as task
import dacapo

# Build/Run Config
HEAP = '512M'
DEFAULT_GC = 'semispace'
BENCH = 'lusearch'
BENCH_SUITE = 'dacapo-9.12'

# Project Config
MACHINE = 'localhost'
OPENJDK = '~/OpenJDK-Rust'



@task.register
def build(gc=DEFAULT_GC, config=False):
    if config:
        task.exec(f'bash configure --disable-warnings-as-errors')
    task.exec(f'cargo +nightly build --no-default-features --features openjdk,{gc}', cwd=f'{OPENJDK}/mmtk')
    task.exec(f'LD_LIBRARY_PATH=$LD_LIBRARY_PATH:{OPENJDK}/mmtk/target/release make', cwd=OPENJDK)

@task.register
def run(gc=DEFAULT_GC, threads=None, n=None):
    java = f'{OPENJDK}/build/linux-x86_64-normal-server-release/jdk/bin/java'
    heap = f'-Xms{HEAP} -Xmx{HEAP} -X:gc:variableSizeHeap=false'
    bm_classpath, bm_entry = dacapo.get_config(BENCH_SUITE, BENCH)
    command = f'{java} -XX:+UseMMTk {heap} -server -cp {bm_classpath} {bm_entry}'
    task.exec(command, machine=MACHINE)


assert MACHINE == 'localhost'
task.run()
