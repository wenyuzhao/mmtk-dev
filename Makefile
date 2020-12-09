vm?=OpenJDK
profile?=fastdebug
gc?=gencopy
benchmark?=avrora
n?=1
heap?=500M

##### Environments #####

export RUST_BACKTRACE=1
export RUSTFLAGS=-Awarnings
export MMTK_PLAN=$(gc)
export RUSTUP_TOOLCHAIN=nightly-2020-07-08
export RUST_LOG=info

##### Constants and derived variables #####

heap_args=-Xms$(heap) -Xmx$(heap)
mmtk_args=-XX:+UseThirdPartyHeap -Dprobes=RustMMTk
probes=/home/wenyuz/MMTk-OpenJDK-Measurements/probes
dacapo_2006=-cp /usr/share/benchmarks/dacapo/dacapo-2006-10-MR2.jar Harness
dacapo_9_12=-Djava.library.path=$(probes) -cp $(probes):$(probes)/probes.jar:/usr/share/benchmarks/dacapo/dacapo-9.12-bach.jar Harness
bm_args=$(dacapo_9_12) -n $(n) -c probe.DacapoBachCallback $(benchmark)

include ./.vscode/$(vm).mk

config: vm-config

build: vm-build

run: vm-run

test: build
	@echo "🟦 Testing: $(conf) (mmtk-plan=$(gc))"
	@make run

clean: vm-clean

variant: profile=release
variant:
	$(MAKE) test
	cp -r ../repos/openjdk/build/linux-x86_64-normal-server-release ~/MMTk-OpenJDK-Measurements/build/$(name)

