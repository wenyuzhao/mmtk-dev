#!/usr/bin/python3
import argparse
import subprocess
import os
import socket

def runHotSpot(java, gc, heap, n, size, t):
    t_args = '' if t is None else f'-t {t}'
    cmd = f'LD_PRELOAD=/home/wenyuz/MMTk-Dev/evaluation/probes/libperf_statistics.so PERF_EVENTS="PERF_COUNT_HW_CPU_CYCLES,PERF_COUNT_HW_INSTRUCTIONS,PERF_COUNT_HW_CACHE_L1D:MISS,PERF_COUNT_HW_CACHE_DTLB:MISS" {java} -XX:-UseCompressedOops -XX:+UnlockExperimentalVMOptions -XX:+Use{gc}GC -XX:MetaspaceSize=1G -XX:+DisableExplicitGC -XX:-UseBiasedLocking -server -XX:-TieredCompilation -XX:+UnlockDiagnosticVMOptions -XX:-InlineObjectCopy -Xcomp -Djava.library.path=/home/wenyuz/MMTk-Dev/evaluation/probes -Dprobes=RustMMTk -agentpath:/home/wenyuz/MMTk-Dev/evaluation/probes/libperf_statistics.so -Xms{heap}M -Xmx{heap}M -cp /usr/share/benchmarks/dacapo/dacapo-evaluation-git-29a657f.jar:/home/wenyuz/MMTk-Dev/evaluation/probes:/home/wenyuz/MMTk-Dev/evaluation/probes/probes.jar Harness -c probe.DacapoChopinCallback -n {n} -s {size} lusearch {t_args} --dump-latency'
    print(cmd)
    return os.WEXITSTATUS(os.system(cmd)) == 0

def runMMTk(java, heap, n, size, t):
    t_args = '' if t is None else f'-t {t}'
    cmd = f'MMTK_PLAN=Immix NURSERY_RATIO=3 MTK_PHASE_PERF_EVENTS="PERF_COUNT_HW_CPU_CYCLES,0,-1;PERF_COUNT_HW_INSTRUCTIONS,0,-1;PERF_COUNT_HW_CACHE_L1D:MISS,0,-1;PERF_COUNT_HW_CACHE_DTLB:MISS,0,-1" {java} -XX:MetaspaceSize=1G -XX:+DisableExplicitGC -XX:-UseBiasedLocking -server -XX:-TieredCompilation -XX:+UnlockDiagnosticVMOptions -XX:-InlineObjectCopy -Xcomp -Djava.library.path=/home/wenyuz/MMTk-Dev/evaluation/probes -Dprobes=RustMMTk -XX:+UseThirdPartyHeap -Xms{heap}M -Xmx{heap}M -cp /usr/share/benchmarks/dacapo/dacapo-evaluation-git-29a657f.jar:/home/wenyuz/MMTk-Dev/evaluation/probes:/home/wenyuz/MMTk-Dev/evaluation/probes/probes.jar Harness -c probe.DacapoChopinCallback -n {n} -s {size} lusearch {t_args} --dump-latency'
    print(cmd)
    return os.WEXITSTATUS(os.system(cmd)) == 0

def run(id, java, gc, heap, n, size, t, out):
    os.system(f'mkdir -p {out}')
    ok = None
    if gc == 'LXR':
        ok = runMMTk(java, heap, n, size, t)
    else:
        ok = runHotSpot(java, gc, heap, n, size, t)
    if ok:
        os.system(f'mv scratch {out}/scratch-{id}')
    return ok

def parseArgs():
    parser = argparse.ArgumentParser(description='latency-curve-gen')
    parser.add_argument('--git', type=str, required=True)
    parser.add_argument('-s', '--size', choices=['default', 'large', 'huge'], default='default')
    parser.add_argument('--hfac', type=float, default=3)
    parser.add_argument('-n', '--iterations', type=int, default=2)
    parser.add_argument('--java', type=str)
    parser.add_argument('-gc', type=str, required=True)
    parser.add_argument('--out', type=str, required=True)
    parser.add_argument('-t', type=int)
    parser.add_argument('-c', type=int)
    parser.add_argument('-id', type=str)
    args = parser.parse_args()
    # minheap
    if args.size == 'default':
        args.minheap = 23
    elif args.size == 'large':
        args.minheap = 122
    elif args.size == 'huge':
        args.minheap = 142
    # heap
    args.heap = args.minheap * args.hfac
    # java
    if args.java is None:
        args.java = f'~/MMTk-Dev/evaluation/configs/lxr-latency-curve/jdk-{args.git}/jdk/bin/java'
    # runid
    # date = subprocess.check_output(['date', '+%y%m%d-%H%M%S']).decode("utf-8").strip()
    if args.id is None:
        args.id = f'{args.gc}-{args.size}-{args.hfac}x'
        if args.t is not None:
            args.id += f'-t{args.t}'
        if args.c is not None:
            args.id += f'-gc{args.c}'

    return args

args = parseArgs()
print(args.out, args.id)
print(args)

run(id=args.id, java=args.java, gc=args.gc, heap=args.heap, n=args.iterations, size=args.size, t=args.t, out=args.out)