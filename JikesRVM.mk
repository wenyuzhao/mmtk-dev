
DACAPO ?= lusearch
HEAP ?= 512M
GC ?= RFastAdaptiveG1

MACHINE ?= localhost
DACAPO_VERSION ?= 9.12
N ?= 1
# GC_THREADS = 1

# Constants

LOCAL_HOME = /home/wenyuz
REMOTE_HOME = /home/wenyuz
LOG_DIR = ./logs
JIKESRVM_ROOT = JikesRVM-Rust

# Derived Variables

SSH_PREFIX = ssh $(MACHINE) -t RUST_BACKTRACE=1
RVM = $(JIKESRVM_ROOT)/dist/$(GC)_x86_64-linux/rvm
DACAPO_JAR = /usr/share/benchmarks/dacapo/dacapo-$(DACAPO_VERSION)-bach.jar
PROBES_JAR = $(REMOTE_HOME)/probes/probes.jar
RVM_ARGS = $(if $(GC_THREADS), -X:gc:threads=$(GC_THREADS)) -Xms$(HEAP) -Xmx$(HEAP) -X:gc:variableSizeHeap=false -server -cp $(PROBES_JAR):$(DACAPO_JAR) -Dprobes=MMTk Harness -c probe.DacapoBachCallback $(DACAPO)



build:
    ifdef NUKE
		@cd $(LOCAL_HOME)/$(JIKESRVM_ROOT) && ./bin/buildit $(MACHINE) $(GC) -j /usr/lib/jvm/java-8-openjdk-amd64 --answer-yes --nuke --clear-cc --clear-cache
    else
		@cd $(LOCAL_HOME)/$(JIKESRVM_ROOT) && ./bin/buildit $(MACHINE) $(GC) -j /usr/lib/jvm/java-8-openjdk-amd64 --answer-yes
    endif

run:
	@for i in $$(seq -w 001 $(N)); do \
       make run-once-impl --no-print-directory log_id=$$i; \
    done

run-once:
	@make run-once-impl --no-print-directory

run-once-impl:
    ifeq ($(or $(log_id), 001), 001)
		@mkdir -p $(LOG_DIR)
        ifeq ($(MACHINE), localhost)
			@echo $(LOCAL_HOME)/$(RVM) $(RVM_ARGS)
  	    else
			@echo $(SSH_PREFIX) $(REMOTE_HOME)/$(RVM) $(RVM_ARGS)
        endif
    endif
    ifeq ($(MACHINE), localhost)
		@RUST_BACKTRACE=1 $(LOCAL_HOME)/$(RVM) $(RVM_ARGS) > $(LOG_DIR)/$(or $(log_id),001).log 2>&1; EXIT=$$? $(MAKE) print-result
    else
		@$(SSH_PREFIX) $(REMOTE_HOME)/$(RVM) $(RVM_ARGS) > $(LOG_DIR)/$(or $(log_id),001).log 2>&1; EXIT=$$? make print-result
    endif

RED='\033[0;31m'
GREEN='\033[0;32m'
RESET='\033[0m' # No Color
print-result:
    ifeq ($(EXIT), 0)
		@echo [$(or $(log_id),001)]: `grep PASS ./logs/$(or $(log_id),001).log | rev | cut -c 6- | rev | cut -c 6-`
    else
		@echo [$(or $(log_id),001)]: ${RED}FAILED!!!${RESET}
    endif

download:
	scp $(MACHINE):$(FILE) ./$(notdir $(FILE))