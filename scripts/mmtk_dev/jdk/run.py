from enum import Enum
import os
from pathlib import Path
from typing import Literal
from mmtk_dev.constants import MMTK_DEV, MMTK_OPENJDK, OPENJDK, DACAPO_CHOPIN, PROBES
from mmtk_dev.jdk.bpf import start_capturing_process
from mmtk_dev.utils import ᐅᐳᐳ
from simple_parsing.helpers.fields import choice
from dataclasses import dataclass
from simple_parsing import field
import shutil

# PERF_EVENTS = "PERF_COUNT_SW_TASK_CLOCK,0,-1;PERF_COUNT_HW_CPU_CYCLES,0,-1;PERF_COUNT_HW_INSTRUCTIONS,0,-1;PERF_COUNT_HW_CACHE_L1D:MISS,0,-1;PERF_COUNT_HW_CACHE_L1I:MISS,0,-1;PERF_COUNT_HW_BRANCH_MISSES,0,-1"

PERF_EVENTS = "PERF_COUNT_SW_TASK_CLOCK,0,-1;PERF_COUNT_HW_CPU_CYCLES,0,-1;PERF_COUNT_HW_CACHE_L1D:MISS,0,-1;PERF_COUNT_HW_CACHE_L1D:ACCESS,0,-1"

# os.environ["MMTK_PHASE_PERF_EVENTS"] = PERF_EVENTS

FORCE_USE_JVMTI_HOOK = False
MAX_CORES = 32  # None

HOTSPOT_GCS = {
    "G1": "-XX:+UseG1GC",
    "Parallel": "-XX:+UseParallelGC",
    "Serial": "-XX:+UseSerialGC",
    "Z": "-XX:+UseZGC",
    "ZGC": "-XX:+UseZGCGC",
    "Shen": "-XX:+UseShenandoahGC",
    "Shenandoah": "-XX:+UseShenandoahGC",
}


class Profile(str, Enum):
    release = "release"
    fastdebug = "fastdebug"
    slowdebug = "slowdebug"


# PGO_TRAINING_BENCHMARKS = ["lusearch", "h2", "cassandra", "tomcat"]
DEFAULT_PGO_TRAINING_BENCHMARKS = ["gcbench"]

ALL_PGO_TRAINING_BENCHMARKS = {
    "lusearch": "50M",
    "h2": "800M",
    "cassandra": "150M",
    "tomcat": "30M",
    "pjbb2005": "220M",
    "gcbench": "20M",
}


@dataclass
class Clean:
    """
    Clean all build outputs

    Example: mmtk-jdk clean
    """

    profile: Profile = Profile.fastdebug
    """The profile to clean"""

    def run(self):
        ᐅᐳᐳ("rm", "-rf", MMTK_OPENJDK / "mmtk" / "target")
        ᐅᐳᐳ("rm", "-rf", MMTK_OPENJDK / "build" / f"linux-x86_64-normal-server-{self.profile.value}")


@dataclass
class Build:
    """
    Build openjdk

    Example: mmtk-jdk build
    """

    profile: Profile = Profile.fastdebug
    """The profile to build"""

    release: bool = field(alias="r", default=False, negative_prefix="--no-")
    """Overwrite --profile and force release build"""

    features: str | None = None
    """Rust features to enable"""

    config: bool = field(default=False, negative_prefix="--no-")
    """Configure OpenJDK before build"""

    exploded: bool = field(default=False, alias="x", negative_prefix="--no-")
    """Exploded build"""

    bundle: bool = field(default=False, negative_prefix="--no-")
    """Create product bundles"""

    asan: bool = field(default=False, negative_prefix="--no-")
    """Enable address sanitizer"""

    pgo_gen: bool = field(default=False, negative_prefix="--no-")
    """Generate PGO profiles"""

    pgo_use: bool = field(default=False, negative_prefix="--no-")
    """Build with PGO profiles"""

    clean: bool = field(default=False, negative_prefix="--no-")
    """Perform clean build"""

    def run(self):
        profile = self.profile.value if not self.release else Profile.release.value
        if self.clean:
            Clean(profile=self.profile).run()
        # Configure when necessary
        if self.clean or self.config or not (OPENJDK / "build" / f"linux-x86_64-normal-server-{profile}").exists():
            asan_flags = ["--enable-asan"] if self.asan else []
            ᐅᐳᐳ("sh", "configure", "--disable-zip-debug-info", "--disable-warnings-as-errors", f"--with-debug-level={profile}", "--with-target-bits=64", "--with-jvm-features=shenandoahgc", *asan_flags, cwd=OPENJDK)
            ᐅᐳᐳ("make", "reconfigure", f"CONF=linux-x86_64-normal-server-{profile}", cwd=OPENJDK)
        # Get target
        if self.exploded:
            assert not self.bundle, "cannot bundle an exploded image"
            target = []
        else:
            target = ["product-bundles"] if self.bundle else ["images"]
            ᐅᐳᐳ("rm", "-f", f"{OPENJDK}/build/linux-x86_64-normal-server-{profile}/bundles/*")
        # Get envs
        env = {}
        if self.features is not None:
            env["GC_FEATURES"] = self.features
        if self.pgo_gen:
            ᐅᐳᐳ("rm", "-rf", "/tmp/pgo-data", cwd=MMTK_DEV)
            env["RUSTFLAGS"] = "-Cprofile-generate=/tmp/pgo-data"
        if self.pgo_use:
            env["RUSTFLAGS"] = "-Cprofile-use=/tmp/pgo-data/merged.profdata"
        if self.asan:
            env["RUSTFLAGS"] = "-Zsanitizer=address"
        # Run
        ᐅᐳᐳ("make", f"CONF=linux-x86_64-normal-server-{profile}", f"THIRD_PARTY_HEAP={MMTK_OPENJDK}/openjdk", *target, env=env, cwd=OPENJDK)


@dataclass
class Threads:
    threads_mu: int | None = None
    threads_gc: int | None = None
    threads_conc_gc: int | None = None


@dataclass
class JVMArgs:
    c1: bool = field(default=True, negative_prefix="--no-")
    """Disable C1 compiler"""

    c2: bool = field(default=True, negative_prefix="--no-")
    """Disable C2 compiler"""

    xcomp: bool = field(default=False, negative_prefix="--no-")
    """Enable -Xcomp"""

    threads: Threads = field(default_factory=Threads)
    """Set number of threads"""

    compressed_oops: bool = field(default=True, negative_prefix="--no-")
    """Enable +XX:+UseCompressedOops"""

    class_unloading: bool = field(default=True, negative_prefix="--no-")
    """Enable class unload. Disabling it will set the metaspace size to a huge value (1G)"""

    biased_locking: bool = field(default=True, negative_prefix="--no-")
    """Enable biased locking"""

    weak_refs: bool = field(default=True, negative_prefix="--no-")
    """Enable weak/soft/phantom/finalizer reference processing"""

    jvm_args: list[str] = field(default_factory=list)
    """Extra JVM args"""

    def get_args(self):
        envs: dict[str, str] = {}
        args: list[str] = ["-XX:+UnlockExperimentalVMOptions", "-XX:+UnlockDiagnosticVMOptions", "-XX:+ExitOnOutOfMemoryError"]
        # Compiler args
        if not self.c1 and not self.c2:
            args.append("-Xint")
        elif not self.c1:
            args.append("-XX:-TieredCompilation")
        elif not self.c2:
            args.append("-XX:TieredStopAtLevel=1")
        # Biased locking
        if not self.biased_locking:
            args.append("-XX:-UseBiasedLocking")
        # class unloading
        if not self.class_unloading:
            args += ["-XX:-ClassUnloading", "-XX:-ClassUnloadingWithConcurrentMark"]
        # -Xcomp
        if self.xcomp:
            args.append("-Xcomp")
        # Compressed oops
        if not self.compressed_oops:
            args += ["-XX:-UseCompressedOops", "-XX:-UseCompressedClassPointers"]
        # Compressed oops
        if not self.weak_refs:
            args += ["-XX:-RegisterReferences"]
            envs["MMTK_NO_REFERENCE_TYPES"] = "true"
            envs["MMTK_NO_FINALIZER"] = "true"
        # Extra
        args += self.jvm_args
        # Dedup
        args = [a for a in args if a.strip() != ""]
        args = list(dict.fromkeys(args))
        return args, envs


@dataclass
class Run:
    """
    Run openjdk

    Example: mmtk-jdk r --gc LXR --heap 100M --bench lusearch --build
    """

    gc: str
    """GC plan. e.g. SemiSpace. Comma-separated list of GC plans also supported. e.g. SemiSpace,MarkSweep"""

    heap: str
    """Heap size. e.g. 100M. This will set both -Xms and -Xmx to the same value."""

    bench: str
    """DaCapo benchmark name. e.g. lusearch"""

    profile: Profile = Profile.fastdebug
    """The profile to build"""

    release: bool = field(alias="r", default=False, negative_prefix="--no-")
    """Overwrite --profile and force release build"""

    iter: int = field(alias="n", default=1)
    """Number of iterations"""

    exploded: bool = field(alias="x", default=False, negative_prefix="--no-")
    """Exploded build"""

    # Optional build args

    build: bool = field(alias="b", default=False, negative_prefix="--no-")
    """Build OpenJDK and MMTk before run"""

    config: bool = field(default=False, negative_prefix="--no-")
    """Configure OpenJDK before build"""

    features: str | None = None
    """Rust features to enable"""

    pgo: bool = field(default=False, negative_prefix="--no-")
    """Run with profile-guided optimization enabled."""

    pgo_benchmarks: str = field(default=",".join(DEFAULT_PGO_TRAINING_BENCHMARKS))
    """Benchmarks to run for PGO trainin, comma separated"""

    # Additional run args

    gdb: bool = field(default=False, negative_prefix="--no-")
    """Launch with GDB"""

    rr: bool = field(default=False, negative_prefix="--no-")
    """Launch with rr record"""

    jdk: Path | None = None
    """Use a different pre-built JDK"""

    jvm: JVMArgs = field(default_factory=JVMArgs)
    """JVM Args"""

    verbose: str = choice("0", "1", "2", "3", alias="v", default="0")
    """Set verbosity level"""

    asan: bool = field(default=False, negative_prefix="--no-")
    """Enable address sanitizer"""

    clean: bool = field(default=False, negative_prefix="--no-")
    """Perform clean build"""

    time_v: bool = field(default=False, negative_prefix="--no-")
    """/bin/time -v wrapper"""

    size: str | None = field(alias="s", default=None)
    """Benchmark size"""

    taskset: int | str | None = None
    """`taskset -c` argument as a string, or the number of cores to use"""

    bundle: bool = field(default=False, negative_prefix="--no-")
    """Create product bundles"""

    bpftrace: str | None = None
    """The name of the generated bpftrace file"""

    def build_jdk(self, pgo_step: Literal["gen", "use"] | None):
        build = Build(
            profile=self.profile,
            release=self.release,
            features=self.features,
            config=self.config,
            exploded=self.exploded,
            # bundle = self.bundle
            asan=self.asan,
            pgo_gen=pgo_step == "gen",
            pgo_use=pgo_step == "use",
            clean=self.clean,
            bundle=self.bundle,
        )
        build.run()

    def __get_wrappers(self):
        # taskset wrapper
        wrappers: list[str] = []
        if self.taskset is not None:
            wrappers += ["taskset", "-c"]
            if isinstance(self.taskset, int):
                wrappers += [f"0-{self.taskset - 1}"]
            else:
                wrappers += [f"{self.taskset}"]
        elif MAX_CORES is not None:
            cpu_count = os.cpu_count()
            assert cpu_count is not None
            cores = min(cpu_count, MAX_CORES)
            wrappers += ["taskset", "-c", f"0-{cores - 1}"]
        # GDB Wrapper
        if self.gdb:
            wrappers += ["rust-gdb", "--args"]
        elif self.rr:
            wrappers += ["rr", "record"]
        # time -v wrapper
        wrappers += ["/bin/time", "-v"] if self.time_v else []
        return wrappers

    def __is_dacapo(self, bench: str):
        return bench in ["avrora", "batik", "biojava", "cassandra", "eclipse", "fop", "graphchi", "h2", "h2o", "jme", "jython", "kafka", "luindex", "lusearch", "pmd", "spring", "sunflow", "tomcat", "tradebeans", "tradesoap", "xalan", "zxing"]

    def __is_pjbb2005(self, bench: str):
        return bench in ["pjbb2005"]

    def __is_gcbench(self, bench: str):
        return bench in ["gcbench"]

    def __gc_and_heap_args(self, gc: str, heap: str | None = None):
        # MMTk or HotSpot GC args
        env: dict[str, str] = {}
        heap_args: list[str] = []
        # Enable a GC
        heap_args.append(HOTSPOT_GCS.get(gc, "-XX:+UseThirdPartyHeap"))
        if gc not in HOTSPOT_GCS:
            env["MMTK_PLAN"] = gc
        # Set GC threads
        if self.jvm.threads.threads_gc is not None:
            env["MMTK_THREADS"] = f"{self.jvm.threads.threads_gc}"
            heap_args.append(f"-XX:ParallelGCThreads={self.jvm.threads.threads_gc}")
        if self.jvm.threads.threads_conc_gc is not None:
            env["MMTK_CONC_THREADS"] = f"{self.jvm.threads.threads_conc_gc}"
            heap_args.append(f"-XX:ConcurrentGCThreads={self.jvm.threads.threads_conc_gc}")
        # Heap size
        heap = heap or self.heap
        heap_args += [f"-Xms{heap}", f"-Xmx{heap}"]
        if not self.jvm.class_unloading:
            heap_args.append("-XX:MetaspaceSize=1G")
        return heap_args, env

    def __common_args(self, gc: str, heap: str | None = None):
        env: dict[str, str] = {
            "RUST_BACKTRACE": "1",
        }
        # MMTk or HotSpot GC args
        gc_jvm_args, gc_env = self.__gc_and_heap_args(gc, heap)
        # wrappers
        wrappers = self.__get_wrappers()
        # JVM Args
        jvm_args, jvm_envs = self.jvm.get_args()
        env = {**env, **gc_env, **jvm_envs}
        jvm_args += ["--add-exports", "java.base/jdk.internal.ref=ALL-UNNAMED"]
        jvm_args += gc_jvm_args
        # Extra
        if self.asan:
            env["ASAN_OPTIONS"] = "handle_segv=0"
        if self.verbose != "0":
            env["MMTK_VERBOSE"] = f"{self.verbose}"
            verbose = int(self.verbose)
            if verbose >= 3 and gc in HOTSPOT_GCS:
                jvm_args += ["-Xlog:gc*=debug"]
            elif verbose >= 2:
                jvm_args += ["-Xlog:gc*"]
        return wrappers, env, jvm_args

    def __java_bin(self):
        profile = self.profile.value if not self.release else Profile.release.value
        jdk_build_dir = f"{OPENJDK}/build/linux-x86_64-normal-server-{str(profile)}"
        java = f"{jdk_build_dir}/jdk/bin/java" if self.exploded else f"{jdk_build_dir}/images/jdk/bin/java"
        if self.jdk is not None:
            java = f"{self.jdk}/bin/java"
        return java

    def __bpftrace(self):
        run = self

        class BPFTracer:
            def __enter__(self):
                if run.bpftrace is not None:
                    ᐅᐳᐳ("sudo", "echo", "''")
                    self.daemon = start_capturing_process(exploded=run.exploded)
                return self

            def __exit__(self, exc_type, exc_value, traceback):
                if run.bpftrace is not None:
                    name = f"{run.gc}-{run.bench}-{run.heap}".lower()
                    if run.bpftrace != "":
                        name = name + "-" + run.bpftrace
                    self.daemon.finalize(name=name)

        return BPFTracer()

    def run_jdk(self, gc: str, bench: str | None = None, heap: str | None = None, iter: int | None = None):
        wrappers, env, jvm_args = self.__common_args(gc, heap)
        java = self.__java_bin()
        iter = iter if iter is not None else self.iter
        if self.__is_dacapo(bench or self.bench):
            # Probe args
            bm_args: list[str] = []
            if gc in HOTSPOT_GCS or FORCE_USE_JVMTI_HOOK:
                if PROBES is not None:
                    jvm_args.append(f"-agentpath:{PROBES}/libperf_statistics_pfm3.so")
                    env["LD_PRELOAD"] = f"{PROBES}/libperf_statistics_pfm3.so"
            if PROBES is not None:
                jvm_args += ["-Dprobes=RustMMTk", f"-Djava.library.path={PROBES}", "-cp", f"{PROBES}:{PROBES}/probes.jar:{DACAPO_CHOPIN}"]
                bm_args += ["-c", "probe.DacapoChopinCallback"]
            else:
                jvm_args += ["-cp", DACAPO_CHOPIN]
            # Benchmark args
            if self.jvm.threads.threads_mu is not None:
                bm_args += ["-t", f"{self.jvm.threads.threads_mu}"]
            if self.size is not None:
                bm_args += ["-s", self.size]
            # Run
            with self.__bpftrace():
                ᐅᐳᐳ(*wrappers, java, *jvm_args, "Harness", "-n", f"{iter}", bench or self.bench, *bm_args, env=env)
        elif self.__is_pjbb2005(bench or self.bench):
            jvm_args += ["-cp", "/usr/share/benchmarks/pjbb2005/jbb.jar:/usr/share/benchmarks/pjbb2005/check.jar"]
            assert not self.bpftrace, "BPFTrace is not supported for pjbb2005"
            ᐅᐳᐳ(*wrappers, java, *jvm_args, "spec.jbb.JBBmain", "-propfile", "/usr/share/benchmarks/pjbb2005/SPECjbb-8x10000.props", "-n", f"{iter}", env=env)
        elif self.__is_gcbench(bench or self.bench):
            jvm_args += ["-jar", MMTK_DEV / "scripts/gcbench/gcbench.jar"]
            assert not self.bpftrace, "BPFTrace is not supported for gcbench"
            if iter > 1:
                print("Warning: gcbench does not support multiple iterations")
            ᐅᐳᐳ(*wrappers, java, *jvm_args, env=env)
        else:
            raise ValueError(f"Unknown benchmark {bench or self.bench}")

    def __fix_pfm_sys_permission_error(self):
        for x in Path(MMTK_OPENJDK / "mmtk/target/x86_64-unknown-linux-gnu/release/build").glob("pfm-sys-*"):
            if x.is_dir():
                shutil.rmtree(x)

    def run(self):
        gcs = self.gc.split(",") if "," in self.gc else [self.gc]
        if self.build:
            if self.pgo:
                self.__fix_pfm_sys_permission_error()
                assert self.profile == Profile.release or self.release, "PGO requires a release build"
                assert not self.asan, "PGO does not work with asan"
                # Build for PGO profile generation
                self.build_jdk(pgo_step="gen")
                # Run a few benchmarks to generate PGO profiles
                pgo_benchmarks = self.pgo_benchmarks.split(",")
                for bench in pgo_benchmarks:
                    for gc in gcs:
                        self.run_jdk(gc=gc, bench=bench, heap=ALL_PGO_TRAINING_BENCHMARKS[bench], iter=5)
                # Merge PGO profiles
                llvm_profdata = Path.home() / ".cargo/bin/rust-profdata"
                ᐅᐳᐳ(llvm_profdata, "merge", "-o", "/tmp/pgo-data/merged.profdata", "/tmp/pgo-data", cwd=MMTK_OPENJDK / "mmtk")
                self.__fix_pfm_sys_permission_error()
                # Build again with PGO profiles
                self.build_jdk(pgo_step="use")
                self.__fix_pfm_sys_permission_error()
            else:
                self.build_jdk(pgo_step=None)
        for gc in gcs:
            self.run_jdk(gc=gc)
        # TODO: cp bench
