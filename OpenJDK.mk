MACHINE ?= localhost
DACAPO ?= lusearch
DACAPO_VERSION ?= 9.12
HEAP ?= 500M
N ?= 1
GC ?= semispace

# Constants

LOCAL_HOME = /home/wenyuz
REMOTE_HOME = /home/wenyuz
LOG_DIR = ../logs
OPENJDK_ROOT = OpenJDK-Rust

# Derived Variables

ENV = LD_LIBRARY_PATH=$$LD_LIBRARY_PATH:$(REMOTE_HOME)/$(OPENJDK_ROOT)/mmtk/target/debug RUST_BACKTRACE=1
DACAPO_JAR = /usr/share/benchmarks/dacapo/dacapo-$(DACAPO_VERSION)-bach.jar
ifneq ($(MACHINE), localhost)
	SSH = ssh $(MACHINE) -t
else
	SSH = bash -c
endif
JAVA = $(REMOTE_HOME)/$(OPENJDK_ROOT)/build/linux-x86_64-normal-server-release/jdk/bin/java

config:
	$(SSH) "cd $(REMOTE_HOME)/$(OPENJDK_ROOT) && bash configure --disable-warnings-as-errors"

build:
    ifneq ($(MACHINE), localhost)
		rsync -a $(LOCAL_HOME)/$(OPENJDK_ROOT)/ $(MACHINE):$(REMOTE_HOME)/$(OPENJDK_ROOT)/
    endif
    ifdef CONFIG
		make config
    endif
	$(SSH) "cd $(REMOTE_HOME)/$(OPENJDK_ROOT)/mmtk && cargo +nightly build --no-default-features --features 'openjdk,$(GC)'"
	$(SSH) "cd $(REMOTE_HOME)/$(OPENJDK_ROOT) && LD_LIBRARY_PATH=$$LD_LIBRARY_PATH:$$PWD/mmtk/target/release make"

run:
	$(SSH) "$(ENV) $(JAVA) -XX:+UseMMTk -jar $(DACAPO_JAR) $(DACAPO)"