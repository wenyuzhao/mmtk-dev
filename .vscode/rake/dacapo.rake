$dacapo_dir = "/usr/share/benchmarks/dacapo"
$dacapo_9_12_jar = "#{$dacapo_dir}/dacapo-9.12-bach.jar"
$dacapo_new_jar = "#{$dacapo_dir}/dacapo-evaluation-git-29a657f.jar"
$dacapo_args = -> (dacapo_jar) { "-Djava.library.path=#{$probes_dir} -cp #{$probes_dir}:#{$probes_jar}:#{dacapo_jar} Harness" }

$probes_dir = "$PWD/evaluation/probes"
$probes_jar = "#{$probes_dir}/probes.jar"

$jvmti_args = "-agentpath:$PWD/evaluation/probes/libperf_statistics.so -Dprobes=RustMMTk"
$jvmti_env = "LD_PRELOAD=$PWD/evaluation/probes/libperf_statistics.so"

perf_events = [
    "PERF_COUNT_HW_CPU_CYCLES",
    "PERF_COUNT_HW_INSTRUCTIONS",
    # "PERF_COUNT_HW_CACHE_LL:MISS",
    "PERF_COUNT_HW_CACHE_L1D:MISS",
    "PERF_COUNT_HW_CACHE_DTLB:MISS",
]
# Intel
# perf_events.append([
#     "PERF_COUNT_HW_CACHE_LL:MISS",
# ])

ENV['PERF_EVENTS'] = perf_events.join(",")

mmtk_perf_events = perf_events.map { |x| "#{x},0,-1" }.join(";")

ENV['MMTK_PHASE_PERF_EVENTS'] = mmtk_perf_events