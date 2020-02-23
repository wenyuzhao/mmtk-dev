BENCH_SUITE = dacapo-9.12
BENCH ?= lusearch
HEAP ?= 512M
GC ?= semispace

MACHINE ?= localhost
N ?= 1

# Constants

LOCAL_HOME = /home/wenyuz
REMOTE_HOME = /home/wenyuz
OPENJDK_ROOT = OpenJDK-Rust
LOG_DIR = ../logs

ifdef RELEASE
    PROFILE=release
    RELEASE_FLAG_OPT = --release
else
    PROFILE=debug
endif

ENV = LD_LIBRARY_PATH=$$LD_LIBRARY_PATH:$(REMOTE_HOME)/$(OPENJDK_ROOT)/mmtk/target/$(PROFILE) RUST_BACKTRACE=1

# Derived Variables

NO_CALLBACK = 1
include Config-Benchmark.mk # Depends on BENCH_SUITE/LOCAL_HOME/REMOTE_HOME/MACHINE


JAVA = $(OPENJDK_ROOT)/build/linux-x86_64-normal-server-release/jdk/bin/java



config:
	$(EXEC) "cd $(EXEC_HOME)/$(OPENJDK_ROOT) && bash configure --disable-warnings-as-errors"

build:
	@make build-impl --no-print-directory

build-impl:
    ifneq ($(MACHINE), localhost)
		rsync -a $(LOCAL_HOME)/$(OPENJDK_ROOT)/ $(MACHINE):$(REMOTE_HOME)/$(OPENJDK_ROOT)/
    endif
    ifdef CONFIG
		make config
    endif
	$(EXEC) "cd $(EXEC_HOME)/$(OPENJDK_ROOT)/mmtk && cargo +nightly build $(RELEASE_FLAG_OPT) --no-default-features --features 'openjdk,$(GC)'"
	$(EXEC) "cd $(EXEC_HOME)/$(OPENJDK_ROOT) && LD_LIBRARY_PATH=$$LD_LIBRARY_PATH:$$PWD/mmtk/target/release make"

run:
	$(EXEC) "$(ENV) $(EXEC_HOME)/$(JAVA) -XX:+UseMMTk -XX:-UseCompressedOops $(BENCHMARK_ENTRY)"

#  gdb -ex 'handle SIGSEGV nostop noprint pass' -ex run -ex bt -ex kill -ex quit  --args /home/wenyuz/OpenJDK-Rust/build/linux-x86_64-normal-server-release/jdk/bin/java -XX:+UseMMTk -XX:-UseCompressedOops -jar /usr/share/benchmarks/dacapo/dacapo-9.12-bach.jar fop
