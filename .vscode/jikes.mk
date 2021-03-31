profile=RBaseBaseSemiSpace
benchmark?=pmd
n?=1
heap?=500M


build_args = --answer-yes --use-third-party-heap=../../ --use-third-party-build-configs=../../jikesrvm/build/configs/ --use-external-source=../../jikesrvm/rvm/src
ifdef quick
    build_args += -q
endif
# /home/wenyuz/MMTk-Dev/evaluation/build/RFastAdaptiveImmix_x86_64-linux/rvm -Xms639M -Xmx639M -X:gc:variableSizeHeap=false -X:vm:errorsFatal=true -X:gc:ignoreSystemGC=true -Dprobes=Replay,RustMMTk32 -X:aos:initial_compiler=base -X:aos:enable_bulk_compile=true -X:aos:enable_recompilation=false -X:aos:cafi=/home/wenyuz/MMTk-Dev/evaluation/advice/avrora.ca -X:aos:dcfi=/home/wenyuz/MMTk-Dev/evaluation/advice/avrora.dc -X:vm:edgeCounterFile=/home/wenyuz/MMTk-Dev/evaluation/advice/avrora.ec -Djava.library.path=/home/wenyuz/MMTk-Dev/evaluation/probes -cp /home/wenyuz/MMTk-Dev/evaluation/probes/probes.jar:/usr/share/benchmarks/dacapo/dacapo-9.12-MR1-bach-java6.jar Harness -c probe.DacapoBachCallback -n 2 avrora

advice_args = -X:vm:errorsFatal=true -X:gc:ignoreSystemGC=true -Dprobes=Replay -X:aos:initial_compiler=base -X:aos:enable_bulk_compile=true -X:aos:enable_recompilation=false -X:aos:cafi=./evaluation/advice/avrora.ca -X:aos:dcfi=./evaluation/advice/avrora.dc -X:vm:edgeCounterFile=./evaluation/advice/avrora.ec
vm_root = mmtk-jikesrvm/repos/jikesrvm
rvm = ./mmtk-jikesrvm/repos/jikesrvm/dist/$(profile)_x86_64-linux/rvm
heap_args=-Xms$(heap) -Xmx$(heap)
_profile_first_char=$(shell echo $(profile) | tail -c 1)
ifeq ($(_profile_first_char),R)
    probes=RustMMTk32
else
    probes=MMTk
endif
mmtk_args=-Dprobes=$(probes)
probes=$(PWD)/evaluation/probes
dacapo_2006=-Djava.library.path=$(probes) -cp $(probes):$(probes)/probes.jar:/usr/share/benchmarks/dacapo/dacapo-2006-10-MR2.jar Harness -c probe.Dacapo2006Callback
dacapo_9_12=-Djava.library.path=$(probes) -cp $(probes):$(probes)/probes.jar:/usr/share/benchmarks/dacapo/dacapo-9.12-bach.jar  Harness -c probe.DacapoBachCallback
bm_args= $(dacapo_9_12) -n $(n) $(benchmark)
export RUST_BACKTRACE=1
export RUSTFLAGS=-Awarnings
export RUST_LOG=info
export RUSTUP_TOOLCHAIN=nightly-2020-12-20



config: config-probe
	cd mmtk-jikesrvm/mmtk && eval `ssh-agent` && ssh-add

build:
	cd $(vm_root) && ./bin/buildit localhost $(profile) $(build_args)

test:
	$(rvm) $(heap_args) $(bm_args)