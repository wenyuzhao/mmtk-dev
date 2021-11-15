#!/usr/bin/env bash
set -e

if [ $# -lt 3 ]; then
    echo "Usage: $0 <git-hash> <size> <hfac> [n=2] [t] [java-path]"
    echo ""
    echo "e.g. ./lagency_dump.sh a9feb14 large 1.5"
    exit
fi

result_moma=fox.moma

branch=$1
size=$2
hfac=$3
n=${4:-2}
java_mmtk="~/MMTk-Dev/evaluation/configs/lxr-latency-curve/jdk-$branch/jdk/bin/java"
java=${5:-$java_mmtk}
t=$6

if [[ -z "$t" ]]; then
    t_args=""
else
    t_args="-t $t"
fi

case "$size" in
default) minheap=23;;
large) minheap=122;;
huge) minheap=142;;
*)
    echo "Unkonwn bnechmark size: $size"
    exit;;
esac

heap=$(python -c "print int(round($minheap * $hfac))")M

run_id=$(date +%Y%m%d-%H%M%S)-$size-${hfac}x-$branch

out=~/MMTk-Dev/_latency_logs/$run_id
mkdir -p ~/MMTk-Dev/_latency_logs/$run_id

echo "jdk: jdk-$branch" > $out/log
echo "benchmark: lusearch" >> $out/log
echo "size: $size (minheap ${minheap}M)" >> $out/log
echo "hfac: ${hfac}X" >> $out/log
echo "run-id: $run_id" >> $out/log
echo "java: $java" >> $out/log
echo "iter: $n" >> $out/log
echo "t: $t" >> $out/log
cat $out/log

set -ex

bench=lusearch

retry() {
    local -r -i max_attempts="$1"; shift
    local -i attempt_num=1
    until "$@"
    do
        if ((attempt_num==max_attempts))
        then
            echo "Attempt $attempt_num failed and there are no more attempts left!"
            return 1
        else
            echo "Attempt $attempt_num failed! Trying again in $attempt_num seconds..."
            sleep $((attempt_num++))
        fi
    done
}

pushd ~/MMTk-Dev

for gc in G1 Shenandoah Parallel; do
    LD_PRELOAD=/home/wenyuz/MMTk-Dev/evaluation/probes/libperf_statistics.so PERF_EVENTS="PERF_COUNT_HW_CPU_CYCLES,PERF_COUNT_HW_INSTRUCTIONS,PERF_COUNT_HW_CACHE_L1D:MISS,PERF_COUNT_HW_CACHE_DTLB:MISS" retry 5 $java -XX:-UseCompressedOops -XX:+UnlockExperimentalVMOptions -XX:+Use${gc}GC -XX:MetaspaceSize=1G -XX:+DisableExplicitGC -XX:-UseBiasedLocking -server -XX:-TieredCompilation -XX:+UnlockDiagnosticVMOptions -XX:-InlineObjectCopy -Xcomp -Djava.library.path=/home/wenyuz/MMTk-Dev/evaluation/probes -Dprobes=RustMMTk -agentpath:/home/wenyuz/MMTk-Dev/evaluation/probes/libperf_statistics.so -Xms$heap -Xmx$heap -cp /usr/share/benchmarks/dacapo/dacapo-evaluation-git-29a657f.jar:/home/wenyuz/MMTk-Dev/evaluation/probes:/home/wenyuz/MMTk-Dev/evaluation/probes/probes.jar Harness -c probe.DacapoChopinCallback -n $n -s $size $bench $t_args --dump-latency
    mv scratch $out/scratch-$gc
done

if [[ "$java" == "$java_mmtk" ]]; then
MMTK_PLAN=Immix NURSERY_RATIO=3 MTK_PHASE_PERF_EVENTS="PERF_COUNT_HW_CPU_CYCLES,0,-1;PERF_COUNT_HW_INSTRUCTIONS,0,-1;PERF_COUNT_HW_CACHE_L1D:MISS,0,-1;PERF_COUNT_HW_CACHE_DTLB:MISS,0,-1" retry 5 $java -XX:MetaspaceSize=1G -XX:+DisableExplicitGC -XX:-UseBiasedLocking -server -XX:-TieredCompilation -XX:+UnlockDiagnosticVMOptions -XX:-InlineObjectCopy -Xcomp -Djava.library.path=/home/wenyuz/MMTk-Dev/evaluation/probes -Dprobes=RustMMTk -XX:+UseThirdPartyHeap -Xms$heap -Xmx$heap -cp /usr/share/benchmarks/dacapo/dacapo-evaluation-git-29a657f.jar:/home/wenyuz/MMTk-Dev/evaluation/probes:/home/wenyuz/MMTk-Dev/evaluation/probes/probes.jar Harness -c probe.DacapoChopinCallback -n $n -s $size $bench $t_args --dump-latency
mv scratch $out/scratch-LXR
fi

popd

rsync -azR --no-i-r -h --info=progress2 ~/./MMTk-Dev/_latency_logs $result_moma:/home/wenyuz/