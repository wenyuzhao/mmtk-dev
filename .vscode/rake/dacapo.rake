$dacapo_dir = "/usr/share/benchmarks/dacapo"
$dacapo_9_12_jar = "#{$dacapo_dir}/dacapo-9.12-bach.jar"
$dacapo_new_jar = "#{$dacapo_dir}/dacapo-evaluation-git-69a704e.jar"
$dacapo_args = -> (dacapo_jar) { "-Djava.library.path=#{$probes_dir} -cp #{$probes_dir}:#{$probes_jar}:#{dacapo_jar} Harness" }

$probes_dir = "$PWD/evaluation/probes"
$probes_jar = "#{$probes_dir}/probes.jar"