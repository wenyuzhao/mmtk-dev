vm_root = ./mmtk-openjdk/repos/openjdk
conf=linux-x86_64-normal-server-$(profile)
vm_args:=-XX:MetaspaceSize=1G
profile?=slowdebug
gc?=gencopy
benchmark?=xalan
n?=1
heap?=500M

# Interpreter only
# common_args=-server -XX:+DisableExplicitGC -Xint
# Int+C1 only
# common_args=-server -XX:+DisableExplicitGC -XX:TieredStopAtLevel=1
# Int+C2 only
vm_args:=$(vm_args) -server -XX:+DisableExplicitGC -XX:-TieredCompilation
# Int+C1+C2
# common_args=-server -XX:+DisableExplicitGC

heap_args=-Xms$(heap) -Xmx$(heap)
mmtk_args=-XX:+UseThirdPartyHeap -Dprobes=RustMMTk
probes=$(PWD)/evaluation/probes
dacapo_2006=-cp /usr/share/benchmarks/dacapo/dacapo-2006-10-MR2.jar Harness
dacapo_9_12=-Djava.library.path=$(probes) -cp $(probes):$(probes)/probes.jar:/usr/share/benchmarks/dacapo/dacapo-9.12-bach.jar Harness
bm_args=$(dacapo_9_12) -n $(n) -c probe.DacapoBachCallback $(benchmark)

export RUST_BACKTRACE=1
export RUSTFLAGS=-Awarnings
export MMTK_PLAN=$(gc)
export RUSTUP_TOOLCHAIN=nightly-2020-12-20
export RUST_LOG=info
export PERF_EVENTS=PERF_COUNT_HW_CACHE_DTLB:MISS,PERF_COUNT_HW_CACHE_ITLB:MISS



config:
	@cd evaluation/probes && make all
	@echo "🟦 Config: $(conf) (mmtk-plan=$(gc))"
	@cd mmtk-openjdk/mmtk && eval `ssh-agent` && ssh-add
	@cd $(vm_root) && sh configure --disable-warnings-as-errors --with-debug-level=$(profile) --with-target-bits=64 --disable-zip-debug-info

build:
	@echo "🟦 Building: $(conf) (mmtk-plan=$(gc))"
	@cd $(vm_root) && make --no-print-directory CONF=$(conf) THIRD_PARTY_HEAP=$$PWD/../../openjdk

run: java=$(vm_root)/build/$(conf)/jdk/bin/java
run:
	$(java) $(vm_args) $(heap_args) $(mmtk_args) $(bm_args)

test: build
	@echo "🟦 Testing: $(conf) (mmtk-plan=$(gc))"
	@make run

clean:
	@cd $(vm_root) && make clean CONF=$(CONF) --no-print-directory

bench-variant: profile=release
bench-variant:
	$(MAKE) test profile=release
	@mkdir -p $(PWD)/evaluation/build
	@cp -r $(vm_root)/build/linux-x86_64-normal-server-release $(PWD)/evaluation/build/$(name)
