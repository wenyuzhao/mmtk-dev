file /usr/lib/jvm/adoptopenjdk-11-hotspot-amd64/bin/java
set environment LD_PRELOAD /home/zixianc/MMTk-Dev/evaluation/probes/native/jvmti_agents/libperf_statistics.so
set environment PERF_EVENTS PERF_COUNT_HW_CPU_CYCLES
handle SIGSEGV pass nostop
r -agentpath:/home/zixianc/MMTk-Dev/evaluation/probes/native/jvmti_agents/libperf_statistics.so -Djava.library.path=/home/zixianc/MMTk-Dev/evaluation/probes -Dprobes=RustMMTk -cp /usr/share/benchmarks/dacapo/dacapo-evaluation-git-69a704e.jar:/home/zixianc/MMTk-Dev/evaluation/probes/ Harness -c probe.DacapoChopinCallback -n 1 fop
