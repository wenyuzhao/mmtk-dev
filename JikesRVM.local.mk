# dacapo-9.12 / dacapo-2006 / pjbb2005
BENCH_SUITE = dacapo-9.12
BENCH ?= lusearch
HEAP ?= 512M
GC ?= RBaseBaseSemiSpace

MACHINE ?= localhost
N ?= 1
# GC_THREADS = 1

# Constants

LOCAL_HOME = /home/wenyuz
REMOTE_HOME = /home/wenyuz
JIKESRVM_ROOT = JikesRVM-Rust
LOG_DIR = ./logs
ENV = RUST_BACKTRACE=1

# Derived Variables
 
include Config-Benchmark.mk # Depends on BENCH_SUITE/LOCAL_HOME/REMOTE_HOME/MACHINE


RVM = $(JIKESRVM_ROOT)/dist/$(GC)_x86_64-linux/rvm
RVM_ARGS = $(if $(GC_THREADS), -X:gc:threads=$(GC_THREADS)) -Xms$(HEAP) -Xmx$(HEAP) -X:gc:variableSizeHeap=false -server $(BENCHMARK_ENTRY)

BUILDIT_ARGS = $(MACHINE) $(GC) -j /usr/lib/jvm/java-8-openjdk-amd64 --answer-yes $(if $(NUKE), --nuke --clear-cc --clear-cache, --quick)



build:
	@cd $(LOCAL_HOME)/$(JIKESRVM_ROOT) && ./bin/buildit $(BUILDIT_ARGS)

run:
	@mkdir -p $(LOG_DIR)
	@echo $(EXEC_HOME)/$(RVM) $(RVM_ARGS)
	@for i in $$(seq -w 001 $(N)); do \
       make run-once --no-print-directory log_id=$$i; \
    done

run-once:
	@$(EXEC) "RUST_BACKTRACE=1 $(EXEC_HOME)/$(RVM) $(RVM_ARGS)" > $(LOG_DIR)/$(or $(log_id),001).log 2>&1; EXIT=$$? $(MAKE) print-result

RED='\033[0;31m'
GREEN='\033[0;32m'
RESET='\033[0m' # No Color
print-result:
    ifeq ($(EXIT), 0)
		@echo [$(or $(log_id),001)]: `grep PASS ./logs/$(or $(log_id),001).log | rev | cut -c 6- | rev | cut -c 6-`
    else
		@echo [$(or $(log_id),001)]: ${RED}FAILED!!!${RESET}
    endif
