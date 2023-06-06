import re 
import math

def pase_file(log):
    values = []
    with open(log, 'r') as f:
        for line in f:
            if '- live size:' in line:
                match = re.search(r'- live size: (\d+)', line)
                if match:
                    values.append(int(match.groups()[0]))
    return math.ceil(float(max(values)) / 1024 / 1024)

def parse_and_report(name, log):
    live_bytes = pase_file(log)
    print(f'{name}: {live_bytes}')

parse_and_report('blaze-blaze', '../lxr-test/logs/blaze-srwww-ls2.log')