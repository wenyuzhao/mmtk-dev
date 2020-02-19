#
# I reserve no legal rights to this software, it is fully in the public
# domain.  Any company or individual may do whatever they wish with this
# software.
#
# Steve Blackburn May 2005, October 2007, November 2008
#
package RunConfig;
use File::Basename;
use Cwd 'abs_path';
require Exporter;
@ISA = qw(Exporter);
@EXPORT = qw(
	$rootdir
	$remotehost
	$remotedir
	$standalonemode
	$targetinvocations
	$heaprange
	$maxinvocations 
	$arch
	$rvm
	$genadvice
	$producegraphs
	$defaultopts
	%booleanopts
	%valueopts
	@gcconfigs
	@benchmarks
	%needsvfb
	%noreplay
	%minheap
    $perfevents
	%sliceHeapSize
	%bmtimeout
	$bmtimeoutmultiplier
	%bmsuite
	%bmexecdir
	%bmargs
	$defaulttimingiteration
    $defaulttasksetmask
    $defaultcpuidmask
	%mmtkstart
	%mmtkend
	%bmdirs
	%jvmroot
);


###############################################################################
#
# Edit these to control the benchmark runner
#
#

#
# Directories
#
($b,$path,$s) = fileparse($0);
$rootdir = abs_path("$path../");
$remotehost = "wenyuz\@squirrel.moma";
$remotedir = $rootdir;          # same directory structure on both machines

#
# Misc variables
#
$standalonemode = 0;            # if 1, then stop daemons (including network!)
$targetinvocations = 50;        # how many invocations of each benchmark?
$defaulttimingiteration = 16;    # which iteration of the benchmark to time
$heaprange = 6;                 # controls x-axis range
$maxinvocations = $targetinvocations;
$arch = "_x86_64-linux";
$genadvice = 0;
$perfevents = "";

#
# Runtime rvm flags
# 

# default options used by all runs

# boolean options
%booleanopts = (
    # Turn off OSR
    "noosr" => "-X:aos:osr_promotion=false -X:opt:guarded_inline=false -X:opt:guarded_inline_interface=false",
	# Perform eager sweeping
	"e" => "-X:gc:eagerCompleteSweep=true",
	# Do a GC whenever system.gc() is called by the application
	"ugc" => "-X:gc:observe_user_gc_hints=true",
	# Do a GC whenever system.gc() is called by the application
	"ig" => "-X:gc:ignoreSystemGC=true",
	# Use the replay compiler (formerly pseudoadaptive)
	"ar" => "-X:aos:aafi=\$advicedir/\$benchmark.aa",
	# Use the replay compiler (formerly pseudoadaptive)
	"r" => "-X:aos:enable_replay_compile=true -X:aos:cafi=\$advicedir/\$benchmark.ca -X:aos:dcfi=\$advicedir/\$benchmark.dc -X:vm:edgeCounterFile=\$advicedir/\$benchmark.ec",
	# Use the warmup replay compiler
	"wr" => "-Dprobes=Replay -X:aos:initial_compiler=base -X:aos:enable_warmup_replay_compile=true -X:aos:enable_recompilation=false -X:aos:cafi=\$advicedir/\$benchmark.ca -X:aos:dcfi=\$advicedir/\$benchmark.dc -X:vm:edgeCounterFile=\$advicedir/\$benchmark.ec",
	"wrz" => "-Dprobes=Replay -X:aos:initial_compiler=base -X:aos:enable_warmup_replay_compile=true -X:aos:enable_recompilation=false -X:aos:cafi=\$advicedir/\$benchmark.ca",
	"wrc" => "-Dprobes=Replay -X:aos:initial_compiler=base -X:aos:enable_warmup_replay_compile=true -X:aos:enable_recompilation=false -X:aos:cafi=\$advicedir/\$benchmark.ca -X:aos:dcfi=\$advicedir/\$benchmark.dc",
	"wre" => "-Dprobes=Replay -X:aos:initial_compiler=base -X:aos:enable_warmup_replay_compile=true -X:aos:enable_recompilation=false -X:aos:cafi=\$advicedir/\$benchmark.ca -X:vm:edgeCounterFile=\$advicedir/\$benchmark.ec",
	# Force (non-adaptive) just in time compilation at baseline
	"bl" => "-X:aos:initial_compiler=base -X:aos:enable_recompilation=false",
	# Force (non-adaptive) just in time compilation at O0
	"o0" => "-X:aos:initial_compiler=opt -X:aos:enable_recompilation=false -X:irc:O0",
	# Force (non-adaptive) just in time compilation at O1
	"o1" => "-X:aos:initial_compiler=opt -X:aos:enable_recompilation=false -X:irc:O1",
	# Force (non-adaptive) just in time compilation at O2
	"o2" => "-X:aos:initial_compiler=opt -X:aos:enable_recompilation=false -X:irc:O2",
	# Gather retired instructions (using perfctr patch)
	"ri" => "-X:gc:perfMetric=RI",
	# Gather L1 cache misses (using perfctr patch)
	"l1d" => "-X:gc:perfMetric=L1D_MISS",
	# Gather L2 cache misses (using perfctr patch)
	"l2" => "-X:gc:perfMetric=L2_MISS",
	# Gather DTLB misses (using perfctr patch)
	"dtlb" => "-X:gc:perfMetric=DTLB",
	# Gather ITLB misses (using perfctr patch)
	"itlb" => "-X:gc:perfMetric=ITLB",
	# Gather L1I misses (using perfctr patch)
	"l1i" => "-X:gc:perfMetric=L1I_MISS",
	# Gather branches (using perfctr patch)
	"br" => "-X:gc:perfMetric=BRANCHES",
	# Gather branch misses (using perfctr patch)
	"brm" => "-X:gc:perfMetric=BRANCH_MISS",
	# Run in server mode
	"s" => "-server",
    # sun perf options (as per Zhao et al Allocation wall paper)
    "sunperf" => "-Xss128K -XX:+UseParallelGC -XX:+UseParallelOldGC -XX:+UseBiasedLocking -XX:+AggressiveOpts",
    # ibm perf options (as per Zhao et al Allocation wall paper)
    "ibmperf" => "-Xjvm:perf -XlockReservation -Xnoloa -XtlhPrefetch -Xgcpolicy:gencon",
    # jrmc perf options: http://www.spec.org/jbb2005/results/res2009q2/jbb2005-20090519-00724.html
    "jrmcperf" => "-XXaggressive -Xgc:genpar -XXgcthreads:8 -XXcallprofiling -XXtlasize:min=4k,preferred=1024k",
    "sgc" => "-XX:+UseSerialGC",
    "rapl" => "-X:gc:useRAPL=true",
    "sjit" => "-Dprobes=StopJIT -Dprobe.stopjit.iteration=".($defaulttimingiteration-2),
	"g1" => "-XX:+UseG1GC",
	"epsilon" => "-XX:+UnlockExperimentalVMOptions -XX:+UseEpsilonGC",
);
# value options
%valueopts = (
	"i" => "iterations",
	"p" => "-X:processors=",
    "sp" => "-X:vm:forceOneCPU=", # single CPU of specified affinity
    # set a bounded nursery size (<int>M)
	"n" => "-X:gc:boundedNursery=",
	"fn" => "-X:gc:fixedNursery=",
	"rr" => "-X:gc:lineReuseRatio=",
    "mn" => "-Xmn",
	"cr" => "-X:gc:defragLineReuseRatio=",
	"cf" => "-X:gc:defragReserveFraction=",
	"fh" => "-X:gc:defragFreeHeadroom=",
	"fhf" => "-X:gc:defragFreeHeadroomFraction=",
	"h" => "-X:gc:defragHeadroom=",
	"hf" => "-X:gc:defragHeadroomFraction=",
	"st" => "-X:gc:defragSimpleSpillThreshold=",
    "cpu" => "cpuidmask",
    "ts" => "taskselmask",
    "sf" => "-X:gc:stressFactor=",
    "otm" => "-XX:OtherThreadMask=",
    "ctm" => "-XX:CompilerThreadMask=",
    "gtm" => "-XX:GCThreadMask=",
    "cpuf" => "cpufreq",
    "ascii" => "-X:powermeter:ascii=",
    "perf" => "-X:gc:perfEvents=",
    "rn" => "-X:aos:enable_replay_compile=true -X:aos:cafi=\$advicedir/\$benchmark.\$replayid.ca -X:aos:dcfi=\$advicedir/\$benchmark.\$replayid.dc -X:vm:edgeCounterFile=\$advicedir/\$benchmark.\$replayid.ec",
);
# configurations
@gcconfigs = (
	"java-11-openjdk-amd64|s|g1",
	"java-11-openjdk-amd64|s|epsilon"
	# "ibm-java-i386-60|s",
	# "jrmc-1.6.0|s",
);


# directories in which productio jvms can be found
%jvmroot = (
    "java-9-openjdk-amd64" => "/usr/lib/jvm/",
    "java-8-openjdk-amd64" => "/usr/lib/jvm/",
	"java-11-openjdk-amd64" => "/usr/lib/jvm/",
	"ibm-java-i386-60" => "/opt",
	"jdk1.7.0" => "/opt",
	"jdk1.6.0" => "/opt",
	"jdk1.5.0" => "/opt",
	"jrmc-1.6.0" => "/opt",
);

# set of benchmarks to be run
@dacapobms = ("luindex", "chart", "fop", "hsqldb", "lusearch", "pmd", "xalan");
@dacapobachbms = ("avrora", "batik", "eclipse", "fop", "h2", "jython", "luindex", "lusearch", "pmd", "sunflow", "tomcat", "tradebeans", "tradesoap", "xalan");
@jksdcapo = ("antlr", "bloat", "chart", "fop", "hsqldb", "jython", "luindex", "lusearch", "pmd", "xalan", "avrora",);
@jksbach = ("avrora", "sunflow");
@jksdacapo = (@dacapobms, @jksbach);
@jvm98bms = ("_202_jess", "_201_compress", "_209_db", "_213_javac", "_222_mpegaudio", "_227_mtrt", "_228_jack");

# @benchmarks = (@jksdacapo, "pjbb2005", @jvm98bms);
@benchmarks = (
	"luindex", "fop", "hsqldb", "pmd", "avrora", "antlr", "h2", "tradebeans", "tradesoap",
	"_202_jess", "_201_compress", "_209_db", "_213_javac", "_222_mpegaudio", "_227_mtrt", "_228_jack",
	"_205_raytrace",
);
#
# Variables below this line should be stable
#

# true if needs a virtual framebuffer
%needsvfb = ("chart" => 1);

# true if has no replay advice
%noreplay = ("eclipse" => 1);

# base heap size for each benchmark: minimum heap using MarkCompact 20060801
%minheap = (
	# values established for immix-asplos-2008 on 20070718 with FastAdaptiveMarkSweep, using 10-iteration replay compilation
    "luindex" => 10 * 19,

    # "chart" => 10 * 500,
    "fop" => 10 * 29, # OK
	"hsqldb" => 10 * 100, # OK
    # "lusearch" => 10 * 500,
	"pmd" => 10 * 265, # (250, 275]
    # "xalan" => 10 * 500,
    "avrora" => 10 * 35, # OK
    # "sunflow" => 10 * 500,
    # "pjbb2005" => 10 * 500,
    "_202_jess" => 10 * 250, # OK

	"_201_compress" => 10 * 8, # OK
    "_209_db" => 10 * 20, # OK
    "_213_javac" => 3, # (0, 3]
    "_222_mpegaudio" => 3, # (0, 3] 
    "_227_mtrt" => 10 * 7, # OK
    "_228_jack" => 10 * 13, # OK
    "_205_raytrace" => 10 * 6, # OK

    "antlr" => 10 * 198, # OK
    "h2" => 10 * 437, # OK
    "tradebeans" => 10 * 191, # OK
    "tradesoap" => 10 * 70, # OK
	# "pjbb2000" => 10 * 10,
);
# heap size used for -s (slice) option (in this example, 1.5 X min heap)
%sliceHeapSize = ();
foreach $bm (keys %minheap) {
    $sliceHeapSize{$bm} = $minheap{$bm}*(1.5);
}

# Timeouts for each benchmark (in seconds, based on time for second iteration runs on Core Duo with MarkSweep
%bmtimeout = (
    "_201_compress" => 8,
    "_202_jess" => 6,
    "_205_raytrace" => 9,
    "_209_db" => 15,
    "_213_javac" => 9,
    "_222_mpegaudio" => 6,
    "_227_mtrt" => 9,
    "_228_jack" => 10,
#              "antlr" => 12,
#              "bloat" => 36,
#              "chart" => 24,
#              "eclipse" => 130,
#              "fop" => 6,
#              "hsqldb" => 7,
#              "jython" => 100,
#              "luindex" => 30,
#              "lusearch" => 20,
#              "pmd" => 23,
#              "xalan" => 20,
    "avrora" => 30,
    "batik" => 30,
    "eclipse" => 120,
    "fop" => 20,
    "h2" => 30,
    "jython" => 100,
    "luindex" => 30,
    "lusearch" => 30,
    "pmd" => 30,
    "sunflow" => 30,
    "tomcat" => 30,
    "tradebeans" => 120,
    "tradesoap" => 120,
    "xalan" => 30,
    "pjbb2005" => 20,
	"pjbb2000" => 50,
);
$bmtimeoutmultiplier = 2;

$benchmarkroot = "/usr/share/benchmarks";

%bmsuite = (
	"_201_compress" => "jvm98",
	"_202_jess" => "jvm98",
	"_205_raytrace" => "jvm98",
	"_209_db" => "jvm98",
	"_213_javac" => "jvm98",
	"_222_mpegaudio" => "jvm98",
	"_227_mtrt" => "jvm98",
	"_228_jack" => "jvm98",
	"avrora" => dacapobach,
	"batik" => dacapobach,
	"eclipse" => dacapobach,
#	    "fop" => dacapobach,  # buggy
	"h2" => dacapobach,
	"jython" => dacapobach,
	"luindex" => dacapobach,
	"lusearch" => dacapobach,
	"pmd" => dacapobach,
	"sunflow" => dacapobach,
	"tomcat" => dacapobach,
	"tradebeans" => dacapobach,
	"tradesoap" => dacapobach,
	"xalan" => dacapobach,
	"antlr" => dacapo,
	"bloat" => dacapo,
	"chart" => dacapo,
#	    "eclipse" => dacapo,
	"fop" => dacapo,
	"hsqldb" => dacapo,
#	    "jython" => dacapo,
#	    "luindex" => dacapo,
#	    "lusearch" => dacapo,
#	    "pmd" => dacapo,
#	    "xalan" => dacapo,
	"pjbb2005" => pjbb2005,
	"pjbb2000" => pjbb2000,
);

# sub-directories from which each benchmark should be run
$tmp = "/tmp/runbms-".$ENV{USER};
%bmexecdir = (
	"jvm98" => "$benchmarkroot/SPECjvm98",
	"dacapo" => $tmp,
	"dacapobach" => $tmp,
	"pjbb2005" => "/tmp/pjbb2005",
	"pjbb2000" => "/tmp/pjbb2000"
);

%bmargs = (
	"jvm98" => "-cp $rootdir/../probes/probes.jar:. SpecApplication -i[#] [bm]",
	"dacapo" => "-cp $rootdir/../probes/probes.jar:$benchmarkroot/dacapo/dacapo-2006-10-MR2.jar Harness -n [#] [bm]",
	"dacapobach" => "-cp $rootdir/../probes/probes.jar:$benchmarkroot/dacapo/dacapo-9.12-bach.jar Harness -n [#] [bm]",
	"pjbb2005" => "-cp $rootdir/../probes/probes.jar:$benchmarkroot/pjbb2005/jbb.jar:$benchmarkroot/pjbb2005/check.jar spec.jbb.JBBmain -propfile $benchmarkroot/pjbb2005/SPECjbb-8x10000.props -n [#]",
	"pjbb2000" => "-cp pseudojbb.jar spec.jbb.JBBmain -propfile SPECjbb-8x12500.props -n [#] [mmtkstart]",
);
