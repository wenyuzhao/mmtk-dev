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
$targetinvocations = 20;        # how many invocations of each benchmark?
$defaulttimingiteration = 2;    # which iteration of the benchmark to time
$heaprange = 21;                 # controls x-axis range
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
	"wr" => "-Dprobes=Replay -X:aos:initial_compiler=base -X:aos:enable_bulk_compile=true -X:aos:enable_recompilation=false -X:aos:cafi=\$advicedir/\$benchmark.ca -X:aos:dcfi=\$advicedir/\$benchmark.dc -X:vm:edgeCounterFile=\$advicedir/\$benchmark.ec",
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
);
# value options
%valueopts = (
	"i" => "iterations",
	"p" => "-X:availableProcessors=",
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
	"FastAdaptiveG1PauseAnalysis_STWMark_NoRemSet_NonGen|s|wr",
	"FastAdaptiveG1PauseAnalysis_STWMark_RemSet_NonGen|s|wr",
	"FastAdaptiveG1PauseAnalysis_STWMark_RemSet_Gen|s|wr",
	"FastAdaptiveG1PauseAnalysis_ConcMark_NoRemSet_NonGen|s|wr",
	"FastAdaptiveG1PauseAnalysis_ConcMark_RemSet_NonGen_Predictor|s|wr",
	"FastAdaptiveG1PauseAnalysis_ConcMark_RemSet_Gen_Predictor|s|wr"
);


# directories in which productio jvms can be found
%jvmroot = (
    "java-9-openjdk-amd64" => "/usr/lib/jvm/",
    "java-8-openjdk-amd64" => "/usr/lib/jvm/",
	"ibm-java-i386-60" => "/opt",
	"jdk1.7.0" => "/opt",
	"jdk1.6.0" => "/opt",
	"jdk1.5.0" => "/opt",
	"jrmc-1.6.0" => "/opt",
);

# set of benchmarks to be run
# @dacapobms = ("antlr", "bloat", "eclipse", "fop", "hsqldb");
@dacapobms = ("antlr", "bloat", "fop");
@dacapobachbms = ("avrora", "jython", "luindex", "lusearch-fix", "eclipse", "pmd", "sunflow", "xalan");
@jksdacapo = (@dacapobms, @dacapobachbms);
@jvm98bms = ("_202_jess", "_201_compress", "_209_db", "_213_javac", "_222_mpegaudio", "_227_mtrt", "_228_jack");

# @dacapobms = ("luindex", "bloat", "chart", "fop", "hsqldb", "lusearch", "pmd", "xalan");
# @dacapobachbms = ("avrora", "batik", "eclipse", "fop", "h2", "jython", "luindex", "lusearch", "pmd", "sunflow", "tomcat", "tradebeans", "tradesoap", "xalan");
# @jksdcapo = ("antlr", "bloat", "chart", "fop", "hsqldb", "jython", "luindex", "lusearch", "pmd", "xalan", "avrora",);
# @jksbach = ("avrora", "sunflow");
# @jksdacapo = (@dacapobms, @jksbach);
# @jvm98bms = ("_202_jess", "_201_compress", "_209_db", "_213_javac", "_222_mpegaudio", "_227_mtrt", "_228_jack");



@benchmarks = (@jksdacapo, "pjbb2005", @jvm98bms);
# @benchmarks = ("chart");

#
# Variables below this line should be stable
#

# true if needs a virtual framebuffer
%needsvfb = ("chart" => 1);

# true if has no replay advice
# %noreplay = ("eclipse" => 1);
%noreplay = ();

# base heap size for each benchmark: minimum heap using MarkCompact 20060801
%minheap = (
# values established for immix-asplos-2008 on 20070718 with FastAdaptiveMarkSweep, using 10-iteration replay compilation
    "_202_jess" => 39,
	"_201_compress" => 38,
    "_209_db" => 48,
    "_213_javac" => 59,
    "_222_mpegaudio" => 36,
    "_227_mtrt" => 46,
    "_228_jack" => 53,
	# DaCapo 9.12
	"avrora" => 60,
	"jython" => 100,
	"luindex" => 54,
	"lusearch" => 75,
	"lusearch-fix" => 75,
	"pmd" => 88,
	"sunflow" => 69,
	"xalan" => 76,
	# DaCapo 2006
    "antlr" => 62,
    "bloat" => 95,
    "eclipse" => 100,
    "fop" => 67,
    "hsqldb" => 168,

	"chart" => 100,

    # "jython" => 40,
    # "luindex" => 22,
    # "lusearch" => 82,
    # "pmd" => 49,
    # "xalan" => 54,
    # "avrora" => 50,
    # "batik" => 50,
    # "h2" => 127,
    # "sunflow" => 54,
    # "tomcat" => 100,  
    # "tradebeans" => 200,
    # "tradesoap" => 200,
    "pjbb2005" => 200,
	# "pjbb2000" => 214,
);

# heap size used for -s (slice) option (in this example, 1.5 X min heap)
%sliceHeapSize = ();
foreach $bm (keys %minheap) {
	$minheap{$bm} = 96;
    $sliceHeapSize{$bm} = 96;
}

# Timeouts for each benchmark (in seconds, based on time for second iteration runs on Core Duo with MarkSweep
%bmtimeout = (
    "_201_compress" => 18,
    "_202_jess" => 16,
    "_205_raytrace" => 19,
    "_209_db" => 25,
    "_213_javac" => 19,
    "_222_mpegaudio" => 16,
    "_227_mtrt" => 19,
    "_228_jack" => 20,
    # "antlr" => 12,
    # "bloat" => 36,
    # "chart" => 24,
    # "eclipse" => 130,
    # "fop" => 6,
    # "hsqldb" => 7,
    # "jython" => 100,
    # "luindex" => 30,
    # "lusearch" => 20,
    # "pmd" => 23,
    # "xalan" => 20,
    "avrora" => 50,
    "batik" => 50,
    "eclipse" => 180,
    "fop" => 40,
    "h2" => 50,
    "jython" => 180,
    "luindex" => 60,
    "lusearch" => 60,
	"lusearch-fix" => 60,
    "pmd" => 60,
    "sunflow" => 60,
    "tomcat" => 30,
    "tradebeans" => 120,
    "tradesoap" => 120,
    "xalan" => 60,
    "pjbb2005" => 60,
	"pjbb2000" => 50,
);
$bmtimeoutmultiplier = 2;

$benchmarkroot = "/usr/share/benchmarks";

%bmsuite = (
	"_201_compress" => "jvm98",
	"_202_jess" => "jvm98",
	"_209_db" => "jvm98",
	"_213_javac" => "jvm98",
	"_222_mpegaudio" => "jvm98",
	"_227_mtrt" => "jvm98",
	"_228_jack" => "jvm98",

	"avrora" => dacapobach,
	"jython" => dacapobach,
	"luindex" => dacapobach,
	"lusearch" => dacapobach,
	"lusearch-fix" => dacapobach,
	"pmd" => dacapobach,
	"sunflow" => dacapobach,
	"xalan" => dacapobach,
	"chart" => dacapo,
	
	"antlr" => dacapo,
	"bloat" => dacapo,
	"eclipse" => dacapo,
	"fop" => dacapo,
	"hsqldb" => dacapo,
	
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
	"jvm98" => "-Dprobes=MMTk -cp $rootdir/probes/probes.jar:. SpecApplication -i[#] [bm]",
	"dacapo" => "-Dprobes=MMTk -cp $rootdir/probes/probes.jar:$benchmarkroot/dacapo/dacapo-2006-10-MR2.jar Harness -c probe.Dacapo2006Callback -n [#] [bm]",
	"dacapobach" => "-Dprobes=MMTk -cp $rootdir/probes/probes.jar:/home/wenyuz/dacapo-9.12-MR1-bach-java6.jar Harness -c MMTkCallback -n [#] [bm]",
	"pjbb2005" => "-Dprobes=MMTk -cp $rootdir/probes/probes.jar:$benchmarkroot/pjbb2005/jbb.jar:$benchmarkroot/pjbb2005/check.jar spec.jbb.JBBmain -propfile $benchmarkroot/pjbb2005/SPECjbb-8x10000.props -c probe.PJBB2005Callback -n [#]",
	"pjbb2000" => "-cp pseudojbb.jar spec.jbb.JBBmain -propfile SPECjbb-8x12500.props -n [#] [mmtkstart]",
);