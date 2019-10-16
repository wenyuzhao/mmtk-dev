# dacapo-9.12 / dacapo-2006 / pjbb2005
BENCH_SUITE = dacapo-9.12
BENCH ?= lusearch
HEAP ?= 512M
# GC ?= FastAdaptiveSemiSpace
GC ?= FastAdaptiveG1BarrierBaseline
# GC ?= FullAdaptiveG1

BUILD_MACHINE ?= elk.moma
RUN_MACHINE ?= bear.moma
N ?= 1
# GC_THREADS = 1

# Constants

LOCAL_HOME = /home/wenyu
REMOTE_HOME = /home/wenyuz
LOG_DIR = ./logs
JIKESRVM_ROOT = Documents/JikesRVM-G1

# Derived Variables

BM_ROOT = /usr/share/benchmarks
ifeq ($(BENCH_SUITE), pjbb2005)
    BENCH_CLASSPATH = $(BM_ROOT)/pjbb2005/jbb.jar:$(BM_ROOT)/pjbb2005/check.jar
    BENCH_ENTRY = spec.jbb.JBBmain
    BENCH_ARGS = -propfile $(BM_ROOT)/pjbb2005/SPECjbb-8x10000.props -c probe.PJBB2005Callback
else
    ifeq ($(BENCH_SUITE), dacapo-2006)
        BENCH_CLASSPATH = $(BM_ROOT)/dacapo/dacapo-2006-10-MR2.jar
    else
        BENCH_CLASSPATH = $(BM_ROOT)/dacapo/dacapo-9.12-bach.jar
    endif
    BENCH_ENTRY = Harness
    BENCH_ARGS = -c MMTkCallback $(BENCH)
endif

SSH_PREFIX = ssh $(RUN_MACHINE) -t RUST_BACKTRACE=1
RVM = $(JIKESRVM_ROOT)/dist/$(GC)_x86_64-linux/rvm
PROBES_JAR = $(REMOTE_HOME)/running/probes/probes.jar
RVM_ARGS = $(if $(GC_THREADS), -X:gc:threads=$(GC_THREADS)) -Xms$(HEAP) -Xmx$(HEAP) -X:gc:variableSizeHeap=false -server -cp $(PROBES_JAR):$(BENCH_CLASSPATH) $(BENCH_ENTRY) $(BENCH_ARGS)

BUILD_COPY = $(if $(RUN_MACHINE), -c $(RUN_MACHINE))
BUILD_HOST_JDK = -j /usr/lib/jvm/java-8-openjdk-amd64
BUILDIT_COMMON_ARGS = $(BUILD_MACHINE) $(GC) $(BUILD_COPY) $(BUILD_HOST_JDK) --answer-yes

build:
    ifdef NUKE
		@cd $(LOCAL_HOME)/$(JIKESRVM_ROOT) && ./bin/buildit $(BUILDIT_COMMON_ARGS) --nuke --clear-cc --clear-cache
    else
		@cd $(LOCAL_HOME)/$(JIKESRVM_ROOT) && ./bin/buildit $(BUILDIT_COMMON_ARGS) --quick
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
        ifeq ($(RUN_MACHINE), localhost)
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
	scp $(RUN_MACHINE):$(FILE) ./$(notdir $(FILE))