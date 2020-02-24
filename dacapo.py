import task_runner as task
import re

BENCH_ROOT = '/usr/share/benchmarks'
PROBES_JAR = '~/running/probes/probes.jar'

def get_config(suite, bm, probes=True):
    cb = '-c MMTkCallback' if probes else ''
    if suite == 'dacapo-2006':
        return (
            f'{PROBES_JAR}:{BENCH_ROOT}/dacapo/dacapo-2006-10-MR2.jar',
            f'Harness {cb} {bm}'
        )
    if suite == 'dacapo-9.12':
        return (
            f'{PROBES_JAR}:{BENCH_ROOT}/dacapo/dacapo-9.12-bach.jar',
            f'Harness{cb} {bm}'
        )
    task.die(f'Unknown benchmark suite `{suite}`')

def check_log_file(log_file):
    with open(log_file, 'r', encoding='utf-8') as f:
        for line in f:
            if re.search('PASSED', line): return line.strip()
        else:
            return None
