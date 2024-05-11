from enum import Enum
import os
from pathlib import Path
from typing import Literal
from mmtk_dev.constants import MMTK_DEV, MMTK_OPENJDK, OPENJDK, DACAPO_CHOPIN, PROBES
from mmtk_dev.utils import ᐅᐳᐳ
from simple_parsing.helpers.fields import choice
from dataclasses import dataclass
from simple_parsing import field, subgroups

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

    threads: Threads = Threads()
    """Set number of threads"""

    compressed_oops: bool = field(default=True, negative_prefix="--no-")
    """Enable +XX:+UseCompressedOops"""

    class_unloading: bool = field(default=True, negative_prefix="--no-")
    """Enable class unload. Disabling it will set the metaspace size to a huge value (1G)"""

    biased_locking: bool = field(default=True, negative_prefix="--no-")
    """Enable biased locking"""

    jvm_args: list[str] = field(default_factory=list)
    """Extra JVM args"""

    def get_args(self):
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
        # Extra
        args += self.jvm_args
        # Dedup
        args = [a for a in args if a.strip() != ""]
        args = list(dict.fromkeys(args))
        return args


@dataclass
class Run:
    """
    Run openjdk

    Example: mmtk-jdk r --gc LXR --heap 100M --bench lusearch --build
    """

    gc: str
    """GC plan. e.g. SemiSpace"""

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

    # Additional run args

    gdb: bool = field(default=False, negative_prefix="--no-")
    """Launch with GDB"""

    rr: bool = field(default=False, negative_prefix="--no-")
    """Launch with rr record"""

    jdk: Path | None = None
    """Use a different pre-built JDK"""

    jvm: JVMArgs = field(default_factory=JVMArgs)
    """JVM Args"""

    verbose: int = choice(0, 1, 2, 3, alias="v", default=0)
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

    def run_jdk(self, bench: str | None = None, heap: str | None = None, iter: int | None = None):
        env: dict[str, str] = {
            "RUST_BACKTRACE": "1",
            "MMTK_NO_REFERENCE_TYPES": "true",
            "MMTK_NO_FINALIZER": "true",
        }
        # MMTk or HotSpot GC args
        heap_args: list[str] = []
        # Enable a GC
        heap_args.append(HOTSPOT_GCS.get(self.gc, "-XX:+UseThirdPartyHeap"))
        if self.gc not in HOTSPOT_GCS:
            env["MMTK_PLAN"] = self.gc
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
        # taskset wrapper
        wrappers = self.__get_wrappers()
        # JVM Args
        jvm_args = self.jvm.get_args()
        # Probe args
        bm_args: list[str] = []
        if self.gc in HOTSPOT_GCS or FORCE_USE_JVMTI_HOOK:
            if PROBES is not None:
                jvm_args.append(f"-agentpath:{PROBES}/libperf_statistics_pfm3.so")
                env["LD_PRELOAD"] = f"{PROBES}/libperf_statistics_pfm3.so"
        if PROBES is not None:
            jvm_args += ["--add-exports", "java.base/jdk.internal.ref=ALL-UNNAMED", "-Dprobes=RustMMTk", f"-Djava.library.path={PROBES}", "-cp", f"{PROBES}:{PROBES}/probes.jar:{DACAPO_CHOPIN}"]
            bm_args += ["-c", "probe.DacapoChopinCallback"]
        else:
            jvm_args += ["--add-exports", "java.base/jdk.internal.ref=ALL-UNNAMED", "-cp", DACAPO_CHOPIN]
        # Benchmark args
        if self.jvm.threads.threads_mu is not None:
            bm_args += ["-t", f"{self.jvm.threads.threads_mu}"]
        if self.size is not None:
            bm_args += ["-s", self.size]
        # Extra
        if self.asan:
            env["ASAN_OPTIONS"] = "handle_segv=0"
        if self.verbose != 0:
            env["MMTK_VERBOSE"] = f"{self.verbose}"
            if self.verbose >= 3:
                jvm_args += ["-Xlog:gc*"]
            elif self.verbose >= 2:
                jvm_args += ["-Xlog:gc"]
        # Run
        profile = self.profile.value if not self.release else Profile.release.value
        jdk_build_dir = f"{OPENJDK}/build/linux-x86_64-normal-server-{str(profile)}"
        java = f"{jdk_build_dir}/jdk/bin/java" if self.exploded else f"{jdk_build_dir}/images/jdk/bin/java"
        if self.jdk is not None:
            java = f"{self.jdk}/bin/java"
        ᐅᐳᐳ(*wrappers, java, *jvm_args, *heap_args, "Harness", "-n", f"{iter or self.iter}", bench or self.bench, *bm_args, env=env)

    def run(self):
        if self.build:
            if self.pgo:
                assert self.profile == Profile.release, "PGO requires a release build"
                assert not self.asan, "PGO does not work with asan"
                # Build for PGO profile generation
                self.build_jdk(pgo_step="gen")
                # Run a few benchmarks to generate PGO profiles
                self.run_jdk(bench="lusearch", heap="200M", iter=5)
                self.run_jdk(bench="h2", heap="1200M", iter=5)
                self.run_jdk(bench="cassandra", heap="800M", iter=5)
                self.run_jdk(bench="tomcat", heap="300M", iter=5)
                # Merge PGO profiles
                ᐅᐳᐳ(MMTK_DEV / "scripts" / "llvm-profdata", "merge", "-o", "/tmp/pgo-data/merged.profdata", "/tmp/pgo-data")
                # Build again with PGO profiles
                self.build_jdk(pgo_step="use")
            else:
                self.build_jdk(pgo_step=None)
        self.run_jdk()
        # TODO: cp bench
