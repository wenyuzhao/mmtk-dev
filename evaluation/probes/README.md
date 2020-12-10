How to use Linux perf counters with OpenJDK
==========================================

1. Download dependencies
 * Install libpfm (http://perfmon2.sourceforge.net).
 * Download dacapo-2006-10-MR2 (https://sourceforge.net/projects/dacapobench/files/archive/2006-10-MR2/), and copy it to ${BENCHMARKS}
 * Download dacapo-9.12-bach.jar (https://sourceforge.net/projects/dacapobench/files/archive/9.12-bach/), and copy it to ${BENCHMARKS}

2. Configure
 * Please set the JDK variable in common.mk (if using JikesRVM, be sure to use a 1.6 JDK)

3. Build
 * If 32-bit libraries are needed, run make with 'OPTION=-m32' (necessary for JikesRVM)

4. Run
 * Dacpo 2006: `./perf_event_launcher PERF_COUNT_HW_CPU_CYCLES,PERF_COUNT_HW_INSTRUCTIONS $(JAVA) -Djava.library.path=`pwd` -Dprobes=PerfEventLauncher -cp probes.jar:$(DACAPO2006JAR) Harness -c probe.Dacapo2006Callback fop`
 * Dacapo Bach: `./perf_event_launcher PERF_COUNT_HW_CPU_CYCLES,PERF_COUNT_HW_INSTRUCTIONS $(JAVA) -Djava.library.path=`pwd` -Dprobes=PerfEventLauncher -cp probes.jar:$(DACAPOBACHJAR) Harness -c probe.DacapoBachCallback fop`
 * Per CPU: `./perf_event_launcher percpu PERF_COUNT_HW_CPU_CYCLES,PERF_COUNT_HW_INSTRUCTIONS $(JAVA) -Djava.library.path=`pwd` -Dprobes=PerfEventLauncher -cp probes.jar:$(DACAPOBACHJAR) Harness -c probe.DacapoBachCallback fop`

### Note
 * Normally, for each counter, you can check whether the counter is scaled (e.g. two many counters on a fixed number of PMU counters)
by checking whether the PERF_FORMAT_TOTAL_TIME_ENABLED is same as PERF_FORMAT_TOTAL_TIME_RUNNING. However, we ignore the checking for
this JNI approach because when counters are created by thread A while disabled/enabled by thread B, Linux kernel does not maintain
those number correctly. Please make sure that you don't create more counters than the number of counters the platform supports.