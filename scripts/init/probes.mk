
probes: evaluation/probes/librust_mmtk_probe.so evaluation/probes/librust_mmtk_probe_32.so evaluation/probes/probes-java6.jar evaluation/probes/probes.jar evaluation/probes/libperf_statistics.so

evaluation/probes/libperf_statistics.so:
	mkdir -p evaluation/probes
	cd evaluation/probes && wget https://github.com/wenyuzhao/lxr-pldi-2022-artifact/releases/download/_/$(@F)

evaluation/probes/%:
	mkdir -p evaluation/probes
	cd evaluation/probes && wget https://github.com/anupli/probes/releases/download/20230127-snapshot/$(@F)
