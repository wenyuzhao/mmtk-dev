import os
from pathlib import Path
import subprocess
import sys
import yaml
from mmtk_dev.constants import MMTK_DEV, EVALUATION_DIR, OPENJDK, USERNAME
from dataclasses import dataclass
from simple_parsing import field
from mmtk_dev.utils import ᐅᐳᐳ
from .run import Run as RunJDK


def __find_config_file(config: str):
    # Find config file
    configs_dir = EVALUATION_DIR / "configs"
    possible_paths = [
        configs_dir / f"{config}.yml",
        configs_dir / f"{config}.yaml",
        configs_dir / f"{config}/config.yml",
        configs_dir / f"{config}/config.yaml",
    ]
    for p in possible_paths:
        if p.is_file():
            return p
    sys.exit(f"❌ Config `{config}` not found!")


@dataclass
class Build:
    """
    Build openjdks for a benchmark config

    Example: mmtk-jdk bench build --config lxr-xput
    """

    config: str
    """Running config name"""

    gc: str = "Immix"
    """GC to test the build"""

    clean: bool = field(default=False, negative_prefix="--no-")
    """Clean the build directory"""

    allow_dirty: bool = field(default=False, negative_prefix="--no-")
    """Allow dirty workspace"""

    def __validate_repos(self):
        def err(s: str):
            sys.exit("❌ " + s) if self.allow_dirty else print("🚨 " + s)

        if os.system(f"cd {MMTK_DEV} && git diff --quiet") != 0:
            err("Current mmtk-dev workspace is dirty!")
        if os.system(f"cd {MMTK_DEV}/mmtk-core && git diff --quiet") != 0:
            err("Current mmtk-core repo is dirty!")
        if os.system(f"cd {MMTK_DEV}/mmtk-openjdk && git diff --quiet") != 0:
            err("Current mmtk-openjdk repo is dirty!")
        if os.system(f"cd {MMTK_DEV}/openjdk && git diff --quiet") != 0:
            err("Current openjdk repo is dirty!")

    def __is_at_commit(self, repo: Path, commit: str) -> bool:
        return os.system(f"cd {repo} && git diff --quiet {commit}") == 0

    def __checkout(self, repo: Path, commit: str):
        if self.__is_at_commit(repo, commit):
            return
        if os.system(f"cd {repo} && git checkout {commit}") != 0:
            sys.exit(f"❌ Failed to checkout {commit} for repo {repo.name}")

    def __build_one(self, runtime_name: str, build_name: str, features: str | None, config: bool):
        try:
            run = RunJDK(gc=self.gc, bench="fop", heap="500M", build=True, release=True, features=features, config=config or self.clean, clean=self.clean)
            run.run()
            self.__copy_jdk_bundle(build_name)
        except BaseException as e:
            sys.exit(f"❌ Failed to build `runtimes.{runtime_name}`!")

    def __copy_jdk_bundle(self, target: str):
        builds_dir = EVALUATION_DIR / "builds"
        builds_dir.mkdir(parents=True, exist_ok=True)
        # Get bundle file
        bundle = (
            subprocess.check_output(
                ["bash", "-c", f"ls {OPENJDK}/build/linux-x86_64-normal-server-release/bundles/*.tar.gz | grep -v -e symbols -e demos"],
                cwd=MMTK_DEV,
            )
            .decode("utf-8")
            .strip()
        )
        # Delete previous builds
        ᐅᐳᐳ("rm", "-rf", builds_dir / target, cwd=MMTK_DEV)
        ᐅᐳᐳ("rm", "-f", builds_dir / f"{target}.tar.gz", cwd=MMTK_DEV)
        # Copy bundle file
        ᐅᐳᐳ("cp", bundle, builds_dir / f"{target}.tar.gz", cwd=MMTK_DEV)
        # Extract and remove bundle file
        ᐅᐳᐳ("mkdir", "-p", builds_dir / target, cwd=MMTK_DEV)
        ᐅᐳᐳ("tar", "-xf", builds_dir / f"{target}.tar.gz", "-C", builds_dir / target, cwd=MMTK_DEV)
        ᐅᐳᐳ("rm", "-f", builds_dir / f"{target}.tar.gz", cwd=MMTK_DEV)

    def run(self):
        self.__validate_repos()
        config_file = __find_config_file(self.config)
        with open(config_file, "r") as file:
            doc = yaml.safe_load(file)
            for runtime_name in doc["runtimes"]:
                commits = doc["runtimes"][runtime_name]["commits"]
                features = doc["runtimes"][runtime_name].get("features")
                # checkout commits
                print(f"🟢 [{runtime_name}]: mmtk-core@{commits['mmtk-core']} mmtk-openjdk@{commits['mmtk-openjdk']} openjdk@{commits['openjdk']} features={features}")
                self.__checkout(MMTK_DEV / "mmtk-core", commits["mmtk-core"])
                self.__checkout(MMTK_DEV / "mmtk-openjdk", commits["mmtk-openjdk"])
                self.__checkout(MMTK_DEV / "openjdk", commits["openjdk"])
                reconfig_jdk = doc["runtimes"][runtime_name].get("reconfigure", False)
                # build and copy target
                features = doc["runtimes"][runtime_name].get("features")
                home: str = os.path.expandvars(doc["runtimes"][runtime_name]["home"])
                if home.endswith("/"):
                    home = home[:-1]
                build_name = os.path.split(os.path.split(home)[0])[1]
                self.__build_one(runtime_name=runtime_name, build_name=build_name, features=features, config=reconfig_jdk)
                assert os.path.isfile(f"{home}/release"), f"❌ Failed to build `runtimes.{runtime_name}`"
                print(f"✅ [{runtime_name}]: Build successful\n\n\n")


@dataclass
class Rsync:
    """
    rsync builds, scripts, and configs to a remote machine

    Example: mmtk-jdk bench rsync --remote bear.moma
    """

    remote: str
    """Remote machine name"""

    remote_user: str = USERNAME
    """Remote user name"""

    def __rsync(self, src: str, dst: str):
        cmd = ["rsync", "-azR", "--no-i-r", "-h", "--info=progress2", src, dst]
        print(f'🔵 {" ".join(cmd)}')
        try:
            subprocess.check_call(cmd, cwd=MMTK_DEV)
        except subprocess.CalledProcessError:
            sys.exit(f'❌ {" ".join(cmd)}')

    def __run_poetry_install(self):
        MMTK_DEV_REL = str(MMTK_DEV).replace(os.path.expanduser("~") + "/", "")
        cmd = ["ssh", f"{self.remote_user}@{self.remote}", f"cd {MMTK_DEV_REL} && poetry install"]
        print(f'🔵 {" ".join(cmd)}')
        try:
            subprocess.check_call(cmd, cwd=MMTK_DEV)
        except subprocess.CalledProcessError:
            sys.exit(f'❌ {" ".join(cmd)}')

    def run(self):
        dst = f"{self.remote_user}@{self.remote}:/home/{self.remote_user}"
        MMTK_DEV_REL = str(MMTK_DEV).replace(os.path.expanduser("~") + "/", "")
        self.__rsync(f"/home/{USERNAME}/./{MMTK_DEV_REL}/evaluation/configs", dst)
        self.__rsync(f"/home/{USERNAME}/./{MMTK_DEV_REL}/evaluation/advice", dst)
        self.__rsync(f"/home/{USERNAME}/./{MMTK_DEV_REL}/evaluation/probes", dst)
        self.__rsync(f"/home/{USERNAME}/./{MMTK_DEV_REL}/evaluation/builds", dst)
        self.__rsync(f"/home/{USERNAME}/./{MMTK_DEV_REL}/evaluation/manager", dst)
        self.__rsync(f"/home/{USERNAME}/./{MMTK_DEV_REL}/evaluation/manager.py", dst)
        self.__rsync(f"/home/{USERNAME}/./{MMTK_DEV_REL}/poetry.lock", dst)
        self.__rsync(f"/home/{USERNAME}/./{MMTK_DEV_REL}/pyproject.toml", dst)
        self.__rsync(f"/home/{USERNAME}/./{MMTK_DEV_REL}/scripts/mmtk_dev", dst)
        self.__run_poetry_install()


@dataclass
class Run:
    """
    Start a benchmark with a running-config

    Example: mmtk-jdk bench run --config lxr-xput --hfac 2x
    """

    config: str
    """Running config name or path to a running config file"""

    hfac: str
    """Heap factor. e.g. 2x or \"12 1 3 4\""""

    log: Path = MMTK_DEV / "running.log"
    """Benchmark log file"""

    workdir: Path | None = None

    def run(self):
        # Find config file
        config_file = self.config if self.config.endswith((".yml", ".yaml")) and Path(self.config).is_file() else __find_config_file(self.config)
        # Get heap args
        hfac = self.hfac.strip().lower()
        if hfac == "1x":
            hfac_args = ["12", "0"]
        elif hfac == "1.3x":
            hfac_args = ["32", "3"]
        elif hfac == "1.4x":
            hfac_args = ["12", "3"]
        elif hfac == "2x":
            hfac_args = ["12", "7"]
        elif hfac == "3x":
            hfac_args = ["12", "12"]
        elif "-" in hfac:
            try:
                hfac_args = [f"{int(x)}" for x in hfac.split("-")]
            except ValueError:
                sys.exit(f"❌ Invalid hfac args `{hfac}`")
        else:
            sys.exit(f"❌ Invalid hfac args `{hfac}`")
        # Run
        os.system(f"pkill -f java -u {USERNAME} -9")
        workdir_args = [] if self.workdir is None else ["--workdir", self.workdir]
        cmd = ["running", "runbms", *workdir_args, "-p", self.config, "./evaluation/results/log", config_file, *hfac_args]
        env = {"BUILDS": f"{EVALUATION_DIR}/builds", "PATH": os.environ["PATH"]}
        print(f'🔵 RUN: {" ".join(cmd)}')
        print(f"🔵 LOG: {self.log}")
        print(f'🔵 BUILDS: {env["BUILDS"]}')
        with open(self.log, "w") as logfile:
            subprocess.check_call(cmd, stdout=logfile, stderr=logfile, cwd=MMTK_DEV, env=env)


@dataclass
class Bench:
    """
    Benchmarking utils

    Sub-commands:
      build       build jdk(s) for benchmarking
      rsync       rsync builds and benchmark configs to a remote machine
      run         run benchmark
    """

    command: Build | Rsync | Run
    """Sub-commands"""

    def run(self):
        self.command.run()
