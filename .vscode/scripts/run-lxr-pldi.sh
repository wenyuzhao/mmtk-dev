set -ex

TRACE_THRESHOLD2=5 LOCK_FREE_BLOCKS=24 MAX_SURVIVAL_MB=128 SURVIVAL_PREDICTOR_WEIGHTED=1 \
RUST_BACKTRACE=1 MMTK_PLAN=Immix ~/jdk-lxr-pldi-2022/jdk/bin/java -XX:+UnlockDiagnosticVMOptions -XX:-InlineObjectCopy -XX:-ClassUnloading -XX:-ClassUnloadingWithConcurrentMark -XX:-RegisterReferences -XX:MetaspaceSize=1G -XX:-UseBiasedLocking -Xms105M -Xmx105M -XX:+UseThirdPartyHeap -XX:-TieredCompilation -Dprobes=RustMMTk -Djava.library.path=/home/wenyuz/MMTk-Dev/evaluation/probes -cp /home/wenyuz/MMTk-Dev/evaluation/probes:/home/wenyuz/MMTk-Dev/evaluation/probes/probes.jar:/usr/share/benchmarks/dacapo/dacapo-evaluation-git-29a657f.jar Harness -n 5 -c probe.DacapoChopinCallback lusearch
