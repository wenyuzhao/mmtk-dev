
RUN_MACHINE = mink.moma
REMOTE_HOME = /home/wenyuz
# RUN_CONFIG = RunConfig-G1-BarrierAnalysis.pm
RUN_CONFIG = RunConfig-G1-RemSetAnalysis.pm
# RUN_CONFIG = RunConfig-G1-PauseAnalysis.pm

BUILD_BASE_DIR = $(REMOTE_HOME)/Projects/JikesRVM-G1/dist
BUILDS = G1BarrierBaseline

HEAP_ARGS = 8 1 3 5 7
# HEAP_ARGS = 8 3
# HEAP_ARGS = 8 1

SSH = ssh $(RUN_MACHINE) -t

# Copy local running folder to remote
# Update `RunConfig.pm`
# Update builds dir
# Build probes
sync:
	@rsync -av ./running/ $(RUN_MACHINE):$(REMOTE_HOME)/running
	@$(SSH) cp $(REMOTE_HOME)/running/bin/$(RUN_CONFIG) $(REMOTE_HOME)/running/bin/RunConfig.pm
	@$(SSH) rsync -av $(BUILD_BASE_DIR)/ $(REMOTE_HOME)/running/build
	# @$(SSH) rsync -av $(REMOTE_HOME)/Projects/JikesRVM/dist/ $(REMOTE_HOME)/running/build
	$(SSH) "cd $(REMOTE_HOME)/running/probes && make probes.jar OPTION=-m32"

run-benchmark: sync
	$(SSH) mkdir -p $(REMOTE_HOME)/running/results
	ssh $(RUN_MACHINE) "nohup $(REMOTE_HOME)/running/bin/runbms $(HEAP_ARGS) > $(REMOTE_HOME)/running/results/nohup.out 2>&1 &"

genadvice: sync
	@rsync -a $(RUN_MACHINE):$(REMOTE_HOME)/running/advice/ ./running/advice-candidates


#  /home/wenyuz/running/build/FastAdaptiveG1BarrierBaseline_x86_64-linux/rvm -X:availableProcessors=1 -Xms248M -X:gc:variableSizeHeap=false -X:vm:errorsFatal=true -X:gc:ignoreSystemGC=true -Dprobes=Replay,MMTk -X:aos:initial_compiler=base -X:aos:enable_warmup_replay_compile=true -X:aos:enable_recompilation=false -X:aos:cafi=/home/wenyuz/running/advice/lusearch.ca -X:aos:dcfi=/home/wenyuz/running/advice/lusearch.dc -cp /home/wenyuz/running/bin/probes/probes.jar:/usr/share/benchmarks/dacapo/dacapo-2006-10-MR2.jar Harness -c probe.Dacapo2006Callback -n 2 lusearch