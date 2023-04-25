from math import ceil
import re 


def pase_file(bm):
    values = []
    with open(f'./logs/{bm}.log', 'r') as f:
        for line in f:
            if '- live size:' in line:
                match = re.search(r'- live size: (\d+)', line)
                if match:
                    values.append(int(match.groups()[0]))
    return ceil(float(max(values) / 1024 / 1024))

BMS_AND_HEAPS = {
    'avrora': '10M',
    'batik': '370M',
    'biojava': '191M',
    'cassandra': '173M',
    'eclipse': '842M',
    'fop': '26M',
    'graphchi': '507M',
    'h2': '1534M',
    'h2o': '165M',
    'jython': '54M',
    'kafka': '400M',
    'luindex': '82M',
    'lusearch': '52M',
    'sunflow': '54M',
    'tomcat': '38M',
    'xalan': '24M',
    'zxing': '195M',

}

for bm, heap in BMS_AND_HEAPS.items():
    live_bytes = pase_file(bm)
    print(f'{bm}: {live_bytes}')