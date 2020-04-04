BM_ROOT = /usr/share/benchmarks
ifeq ($(BENCH_SUITE), pjbb2005)
    BENCH_JAR = $(BM_ROOT)/pjbb2005/jbb.jar:$(BM_ROOT)/pjbb2005/check.jar
    BENCH_ENTRY = spec.jbb.JBBmain
    BENCH_ARGS = -propfile $(BM_ROOT)/pjbb2005/SPECjbb-8x10000.props $(if $(NO_CALLBACK), , -c probe.PJBB2005Callback)
else
    ifeq ($(BENCH_SUITE), dacapo-2006)
        BENCH_JAR = $(BM_ROOT)/dacapo/dacapo-2006-10-MR2.jar
    else
        BENCH_JAR = $(BM_ROOT)/dacapo/dacapo-9.12-bach.jar
    endif
    BENCH_ENTRY = Harness
    BENCH_ARGS = $(if $(NO_CALLBACK), , -c MMTkCallback) $(BENCH)
endif

PROBES_JAR = $(REMOTE_HOME)/running/probes/probes.jar

BENCHMARK_ENTRY = -cp $(PROBES_JAR):$(BENCH_JAR) $(BENCH_ENTRY) $(BENCH_ARGS)


ifeq ($(MACHINE), localhost)
    EXEC = bash -c
	EXEC_HOME = $(LOCAL_HOME)
else
    EXEC = ssh $(MACHINE) -t
	EXEC_HOME = $(REMOTE_HOME)
endif