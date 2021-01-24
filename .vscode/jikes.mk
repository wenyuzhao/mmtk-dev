profile=RBaseBaseSemiSpace
benchmark?=xalan
n?=1
heap?=500M



vm_root = mmtk-jikesrvm/repos/jikesrvm
rvm = ./mmtk-jikesrvm/repos/jikesrvm/dist/$(profile)_x86_64-linux/rvm
heap_args=-Xms$(heap) -Xmx$(heap)
mmtk_args=-Dprobes=RustMMTk
probes=$(PWD)/evaluation/probes
dacapo_2006=-cp /usr/share/benchmarks/dacapo/dacapo-2006-10-MR2.jar Harness
dacapo_9_12=-Djava.library.path=$(probes) -cp $(probes):$(probes)/probes.jar:/usr/share/benchmarks/dacapo/dacapo-9.12-bach.jar Harness
bm_args=$(dacapo_9_12) -n $(n) $(benchmark)
export RUST_BACKTRACE=1
export RUSTFLAGS=-Awarnings
export RUST_LOG=info
export RUSTUP_TOOLCHAIN=nightly-2020-12-20



config:
	cd mmtk-jikesrvm/mmtk && eval `ssh-agent` && ssh-add

build:
	cd $(vm_root) && ./bin/buildit localhost $(profile) --answer-yes --use-third-party-heap=../../ --use-third-party-build-configs=../../jikesrvm/build/configs/ --use-external-source=../../jikesrvm/rvm/src

test:
	$(rvm) $(heap_args) $(bm_args)