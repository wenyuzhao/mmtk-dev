#!/usr/bin/env python3
import task_runner as task
import dacapo

# Build/Run Config
HEAP = '512M'
DEFAULT_GC = 'BaseBaseSemiSpace'
BENCH = 'lusearch'
BENCH_SUITE = 'dacapo-9.12'

# Project Config
MACHINE = 'elk.moma'
JIKESRVM = '~/Projects/JikesRVM-Rust'



@task.register
def build(gc=DEFAULT_GC, nuke=False):
    build_nuke = '--nuke --clear-cc --clear-cache'
    build_quick = '--quick'
    task.exec(
        f'./bin/buildit {MACHINE} {gc} --answer-yes {build_nuke if nuke else build_quick}',
        cwd = JIKESRVM,
    )

@task.register
def run(gc=DEFAULT_GC, threads=None, n=None):
    gc_threads = f'-X:gc:threads={threads}' if threads is not None else ''
    heap = f'-Xms{HEAP} -Xmx{HEAP} -X:gc:variableSizeHeap=false'
    bm_classpath, bm_entry = dacapo.get_config(BENCH_SUITE, BENCH)
    command = f'dist/{gc}_x86_64-linux/rvm {gc_threads} {heap} -server -cp {bm_classpath} {bm_entry}'
    if n is None:
        task.exec(command, machine=MACHINE, cwd=JIKESRVM)
    else:
        for i in range(int(n)):
            log_id, log_file = f'{i:03}', f'{task.LOG_DIR}/{i:03}.log'
            task.exec(command, machine=MACHINE, cwd=JIKESRVM, stdout=log_file, no_check=True)
            print(f'#{log_id}: {dacapo.check_log_file(log_file) or "FAILED !!!"}')



task.run()
