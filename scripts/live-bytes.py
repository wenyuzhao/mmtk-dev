import os


def run_one_benchmark(bench: str, heap: str):
    java = '/home/wenyuz/MMTk-Dev/openjdk/build/linux-x86_64-normal-server-release/images/jdk/bin/java'
    cmd = f'''
        MMTK_PLAN=LXR MMTK_VERBOSE=2 {java} -server -Djava.library.path=/home/wenyuz/MMTk-Dev/evaluation/probes -Dprobes=RustMMTk -XX:+UseThirdPartyHeap -Xms{heap} -Xmx{heap} --add-exports java.base/jdk.internal.ref=ALL-UNNAMED -cp /usr/share/benchmarks/dacapo/dacapo-evaluation-git-04132797.jar:/home/wenyuz/MMTk-Dev/evaluation/probes:/home/wenyuz/MMTk-Dev/evaluation/probes/probes.jar Harness -c probe.DacapoChopinCallback -n 5 -s default {bench}
    '''
    log = f'/home/wenyuz/MMTk-Dev/logs/{bench}.log'
    success = False
    for i in range(3):
        print(f'RUN {bench} #{i}')
        if os.system(cmd.strip() + f' > {log} 2>&1') == 0:
            success = True
            break

# def 

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
    run_one_benchmark(bm, heap)