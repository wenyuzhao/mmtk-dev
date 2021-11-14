set -ex

run_id=2
branch=ceece056

# java=~/MMTk-Dev/evaluation/configs/lxr-latency-curve/jdk-$branch/jdk/bin/java
java=/home/wenyuz/MMTk-Dev/evaluation/configs/lxr-modest-heap-conc/jdk-ceece056/jdk/bin/java
hs_args='-server -XX:-UseCompressedOops -XX:+DisableExplicitGC -XX:-TieredCompilation -Xcomp -XX:+UnlockExperimentalVMOptions -XX:+UnlockDiagnosticVMOptions -Xms70M -Xmx70M -XX:-UseBiasedLocking -XX:MetaspaceSize=1G -XX:-InlineObjectCopy '
dacapo='-jar /usr/share/benchmarks/dacapo/dacapo-evaluation-git-29a657f.jar'
dacapo_args='-n 5 -s default lusearch --dump-latency'
# wrapper='taskset -c 0-7'

pushd ~/MMTk-Dev

for GC in G1 Shenandoah Parallel; do
    LD_PRELOAD=/home/wenyuz/MMTk-Dev/evaluation/probes/libperf_statistics.so PERF_EVENTS="PERF_COUNT_HW_CPU_CYCLES,PERF_COUNT_HW_INSTRUCTIONS,PERF_COUNT_HW_CACHE_L1D:MISS,PERF_COUNT_HW_CACHE_DTLB:MISS" /home/wenyuz/MMTk-Dev/evaluation/configs/lxr-modest-heap-conc/jdk-ceece056/jdk/bin/java -XX:-UseCompressedOops -XX:+UnlockExperimentalVMOptions -XX:+Use${GC}GC -XX:MetaspaceSize=1G -XX:+DisableExplicitGC -XX:-UseBiasedLocking -server -XX:-TieredCompilation -Xcomp -Djava.library.path=/home/wenyuz/MMTk-Dev/evaluation/probes -Dprobes=RustMMTk -agentpath:/home/wenyuz/MMTk-Dev/evaluation/probes/libperf_statistics.so -Xms70M -Xmx70M -cp /usr/share/benchmarks/dacapo/dacapo-evaluation-git-29a657f.jar:/home/wenyuz/MMTk-Dev/evaluation/probes:/home/wenyuz/MMTk-Dev/evaluation/probes/probes.jar Harness -c probe.DacapoChopinCallback -n 5 -s default lusearch
    mv scratch ~/MMTk-Dev/_logs/scratch-$GC
done

# LD_PRELOAD=/home/wenyuz/MMTk-Dev/evaluation/probes/libperf_statistics.so PERF_EVENTS="PERF_COUNT_HW_CPU_CYCLES,PERF_COUNT_HW_INSTRUCTIONS,PERF_COUNT_HW_CACHE_L1D:MISS,PERF_COUNT_HW_CACHE_DTLB:MISS" $java -XX:-UseCompressedOops -XX:+UnlockExperimentalVMOptions -XX:+UseG1GC -XX:MetaspaceSize=1G -XX:+DisableExplicitGC -XX:-UseBiasedLocking -server -XX:-TieredCompilation -Xcomp -Djava.library.path=/home/wenyuz/MMTk-Dev/evaluation/probes -Dprobes=RustMMTk -agentpath:/home/wenyuz/MMTk-Dev/evaluation/probes/libperf_statistics.so -Xms70M -Xmx70M -cp /usr/share/benchmarks/dacapo/dacapo-evaluation-git-29a657f.jar:/home/wenyuz/MMTk-Dev/evaluation/probes:/home/wenyuz/MMTk-Dev/evaluation/probes/probes.jar Harness -c probe.DacapoChopinCallback -n 5 -s default lusearch
MMTK_PLAN=Immix MMTK_PHASE_PERF_EVENTS="PERF_COUNT_HW_CPU_CYCLES,0,-1;PERF_COUNT_HW_INSTRUCTIONS,0,-1;PERF_COUNT_HW_CACHE_L1D:MISS,0,-1;PERF_COUNT_HW_CACHE_DTLB:MISS,0,-1" NURSERY_RATIO=3 /home/wenyuz/MMTk-Dev/evaluation/configs/lxr-modest-heap-conc/jdk-ceece056/jdk/bin/java -XX:MetaspaceSize=1G -XX:+DisableExplicitGC -XX:-UseBiasedLocking -server -XX:-TieredCompilation -Xcomp -Djava.library.path=/home/wenyuz/MMTk-Dev/evaluation/probes -Dprobes=RustMMTk -XX:+UseThirdPartyHeap -Xms70M -Xmx70M -cp /usr/share/benchmarks/dacapo/dacapo-evaluation-git-29a657f.jar:/home/wenyuz/MMTk-Dev/evaluation/probes:/home/wenyuz/MMTk-Dev/evaluation/probes/probes.jar Harness -c probe.DacapoChopinCallback -n 5 -s default lusearch
# MMTK_PLAN=Immix NURSERY_RATIO=3 $java $hs_args -XX:+UseThirdPartyHeap $dacapo $dacapo_args
mv scratch ~/MMTk-Dev/_logs/scratch-LXR

popd

# rsync -azR --no-i-r -h --info=progress2 ~/./MMTk-Dev/_log fox.moma:/home/wenyuz/./MMTk-Dev/_log-$run_id