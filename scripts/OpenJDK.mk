MACHINE ?= ox.moma
DACAPO ?= lusearch
DACAPO_VERSION ?= 9.12
HEAP ?= 500M
N ?= 1
GC ?= semispace

# Constants

LOCAL_HOME = /home/wenyu
REMOTE_HOME = /home/wenyuz
LOG_DIR = ../logs
OPENJDK_ROOT = Projects/OpenJDK

# Derived Variables

SSH = ssh $(MACHINE) -t RUST_BACKTRACE=1

build:
	rsync -a $(LOCAL_HOME)/$(OPENJDK_ROOT)/ $(ox.moma):$(REMOTE_HOME)/$(OPENJDK_ROOT)/
    ifdef CONFIG
		$(SSH) "cd $(REMOTE_HOME)/$(OPENJDK_ROOT) && bash configure --disable-warnings-as-errors"
    endif
	$(SSH) "cd $(REMOTE_HOME)/$(OPENJDK_ROOT)/mmtk && cargo +nightly build --release --no-default-features --features 'openjdk,$(GC)'"
	$(SSH) "cd $(REMOTE_HOME)/$(OPENJDK_ROOT) && LD_LIBRARY_PATH=$$LD_LIBRARY_PATH:$$PWD/mmtk/target/release make"

run:
	