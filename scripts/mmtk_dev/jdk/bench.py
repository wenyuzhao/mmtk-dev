import os
from pathlib import Path
import subprocess
import sys
from typing import Any
import yaml
from mmtk_dev.constants import MMTK_DEV, EVALUATION_DIR, OPENJDK, USERNAME
from dataclasses import dataclass
from simple_parsing import field
from mmtk_dev.utils import ᐅᐳᐳ
from .run import Run as RunJDK, Build as BuildJDK
import re
import shlex


def _find_config_file(config: str):
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

    reconfigure: bool = field(default=False, negative_prefix="--no-")
    """reconfigure the build directory"""

    allow_dirty: bool = field(default=False, negative_prefix="--no-")
    """Allow dirty workspace"""

    def __validate_repos(self):
        def err(s: str):
            sys.exit("❌ " + s) if not self.allow_dirty else print("🚨 " + s)

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
        if os.system(f"cd {repo} && git checkout {commit} --force") != 0:
            sys.exit(f"❌ Failed to checkout {commit} for repo {repo.name}")

    def __build_one(self, runtime_name: str, build_name: str, features: str | None, exploded: bool, test_command: str | None):
        try:
            if test_command is None:
                run = RunJDK(gc=self.gc, bench="fop", heap="500M", build=True, release=True, features=features, config=self.reconfigure or self.clean, clean=self.clean, bundle=not exploded, exploded=exploded)
                run.run()
            else:
                build = BuildJDK(release=True, features=features, config=self.reconfigure or self.clean, clean=self.clean, bundle=not exploded, exploded=exploded)
                build.run()
                result = os.system(test_command)
                assert result == 0, f"❌ Test command failed with exit code {result}"

            if exploded:
                self.__copy_jdk_bundle_exploded(build_name)
            else:
                self.__copy_jdk_bundle(build_name)
        except BaseException as e:
            sys.exit(f"❌ Failed to build `runtimes.{runtime_name}`!")

    def __copy_jdk_bundle_exploded(self, target: str):
        builds_dir = EVALUATION_DIR / "builds"
        builds_dir.mkdir(parents=True, exist_ok=True)
        # Delete previous builds
        ᐅᐳᐳ("rm", "-rf", builds_dir / target)
        ᐅᐳᐳ("rm", "-f", builds_dir / f"{target}.tar.gz")
        # Copy exploded jdk folder
        ᐅᐳᐳ("cp", "-r", OPENJDK / "build" / "linux-x86_64-normal-server-release", builds_dir / target)

    def __copy_jdk_bundle(self, target: str):
        builds_dir = EVALUATION_DIR / "builds"
        builds_dir.mkdir(parents=True, exist_ok=True)
        # Get bundle file
        bundle = subprocess.check_output(["bash", "-c", f"ls {OPENJDK}/build/linux-x86_64-normal-server-release/bundles/*.tar.gz | grep -v -e symbols -e demos"], cwd=MMTK_DEV).decode("utf-8").strip()
        # Delete previous builds
        ᐅᐳᐳ("rm", "-rf", builds_dir / target)
        ᐅᐳᐳ("rm", "-f", builds_dir / f"{target}.tar.gz")
        # Copy bundle file
        ᐅᐳᐳ("cp", bundle, builds_dir / f"{target}.tar.gz")
        # Extract and remove bundle file
        ᐅᐳᐳ("mkdir", "-p", builds_dir / target)
        ᐅᐳᐳ("tar", "-xf", builds_dir / f"{target}.tar.gz", "-C", builds_dir / target)
        ᐅᐳᐳ("rm", "-f", builds_dir / f"{target}.tar.gz")

    def __check_builds(self, runtimes: Any):
        builds: set[str] = set()
        for runtime_name, runtime in runtimes.items():
            home: str | None = runtime.get("home")
            assert home is not None, f"❌ `runtimes.{runtime_name}.home` is not defined"
            assert home not in builds, f"❌ Duplicated value for `runtimes.{runtime_name}.home`: {home}"
            builds.add(home)
            exploded: bool = runtime.get("exploded", False)
            if exploded:
                assert home.endswith("/jdk"), f"❌ Invalid value for `runtimes.{runtime_name}.home`: {home} (must end with /jdk for exploded builds)"
            else:
                jdk_folder_name = home.split("/")[-1]
                assert re.match(r"jdk-\d+\.\d+\.\d+", jdk_folder_name), f"❌ Invalid value for `runtimes.{runtime_name}.home`: {home} (must end with /jdk-<version>)"

    def run(self):
        os.environ["BUILDS"] = f"{EVALUATION_DIR}/builds"
        self.__validate_repos()
        config_file = _find_config_file(self.config)
        with open(config_file, "r") as file:
            doc = yaml.safe_load(file)
            self.__check_builds(doc["runtimes"])
            for runtime_name, runtime in doc["runtimes"].items():
                assert "commits" in runtime, f"❌ `runtimes.{runtime_name}.commits` is not defined"
                commits = runtime["commits"]
                if commits is None:
                    print(f"✅ [{runtime_name}]: Skipping build\n\n\n")
                    continue
                features = runtime.get("features")
                exploded = runtime.get("exploded", False)
                test_command = runtime.get("test-command")
                # checkout commits
                print(f"🟢 [{runtime_name}]: mmtk-core@{commits['mmtk-core']} mmtk-openjdk@{commits['mmtk-openjdk']} openjdk@{commits['openjdk']} features={features}")
                self.__checkout(MMTK_DEV / "mmtk-core", commits["mmtk-core"])
                self.__checkout(MMTK_DEV / "mmtk-openjdk", commits["mmtk-openjdk"])
                self.__checkout(MMTK_DEV / "openjdk", commits["openjdk"])
                # build and copy target
                features = runtime.get("features")
                home: str = os.path.expandvars(runtime["home"])
                if home.endswith("/"):
                    home = home[:-1]
                build_name = os.path.split(os.path.split(home)[0])[1]
                self.__build_one(runtime_name=runtime_name, build_name=build_name, features=features, exploded=exploded, test_command=test_command)
                assert os.path.isfile(f"{home}/release"), f"❌ Failed to build `runtimes.{runtime_name}`: {home}/release does not exist"
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
        cmd = ["ssh", f"{self.remote_user}@{self.remote}", f"cd {MMTK_DEV_REL} && ~/.local/bin/poetry install"]
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
        self.__rsync(f"/home/{USERNAME}/./{MMTK_DEV_REL}/poetry.lock", dst)
        self.__rsync(f"/home/{USERNAME}/./{MMTK_DEV_REL}/pyproject.toml", dst)
        self.__rsync(f"/home/{USERNAME}/./{MMTK_DEV_REL}/scripts/mmtk_dev", dst)
        self.__rsync(f"/home/{USERNAME}/./{MMTK_DEV_REL}/README.md", dst)
        self.__run_poetry_install()


@dataclass
class Run:
    """
    Start a benchmark with a running-config

    Example: mmtk-jdk bench run --config lxr-xput --hfac 2x
    """

    config: str
    """Running config name or path to a running config file"""

    hfac: str | None = None
    """Heap factor. e.g. 2x or \"12 1 3 4\""""

    log: Path = MMTK_DEV / "running.log"
    """Benchmark log file"""

    workdir: Path | None = None

    def __get_hfac_args(self, config: dict[str, Any]) -> list[str]:
        if self.hfac is None:
            if "hfac" not in config or not isinstance(config["hfac"], str):
                sys.exit(f"❌ `hfac` is not defined in both command line and config file")
            hfac = config["hfac"].strip().lower()
        else:
            hfac = self.hfac.strip().lower()
        if hfac == "1x":
            return ["12", "0"]
        elif hfac == "1.3x":
            return ["32", "7"]
        elif hfac == "1.4x":
            return ["12", "3"]
        elif hfac == "2x":
            return ["12", "7"]
        elif hfac == "3x":
            return ["12", "12"]
        elif "-" in hfac:
            try:
                return [f"{int(x)}" for x in hfac.split("-")]
            except ValueError:
                sys.exit(f"❌ Invalid hfac args `{hfac}`")
        else:
            sys.exit(f"❌ Invalid hfac args `{hfac}`")

    def __get_command(self, config: dict[str, Any], config_file: Path, config_name: str) -> list[str]:
        if "command" in config:
            assert self.hfac is None, "❌ `hfac` is not supported with custom command"
            assert "hfac" not in config, "❌ `hfac` is not supported with custom command"
            raw_cmd = config["command"]
            if isinstance(raw_cmd, str):
                raw_cmd_list: list[str] = shlex.split(raw_cmd)
            elif isinstance(raw_cmd, list):
                raw_cmd_list: list[str] = raw_cmd
            else:
                sys.exit(f"❌ Invalid command: {raw_cmd}")
            for arg in raw_cmd_list:
                if not isinstance(arg, str):
                    sys.exit(f"❌ Invalid command: {raw_cmd}")
            cmd = [os.path.expanduser(os.path.expandvars(arg)) for arg in raw_cmd_list]
        else:
            # Get heap args
            hfac_args = self.__get_hfac_args(config)
            # Run
            os.system(f"pkill -f java -u {USERNAME} -9")
            workdir_args = [] if self.workdir is None else ["--workdir", self.workdir]
            cmd: list[str] = ["running", "runbms", *workdir_args, "-p", config_name, "./evaluation/results/log", str(config_file), *hfac_args]
        return cmd

    def __generate_config_name(self, config_file: Path):
        # If not under configs directory, use the filename
        configs_dir = EVALUATION_DIR / "configs"
        if not str(config_file).startswith(str(configs_dir) + "/"):
            return config_file.stem
        # Config file name without extension
        stem = config_file.stem
        # 1. Backward compatibility: for $configs_dir/<name>/config.yml, use <name>
        if stem == "config" and config_file.parent.parent == configs_dir:
            return config_file.parent.name
        # 2. For $configs_dir/<name>.yml, use <name>
        if config_file.parent == configs_dir:
            return stem
        # 3. For $configs_dir/<project...>/<name>.yml, use [<project...>]:<name>
        projects: list[str] = []
        x = config_file
        while x.parent != configs_dir:
            projects.insert(0, x.parent.name)
            x = x.parent
        project_name = ".".join(projects)
        return f"[{project_name}]{stem}"

    def run(self):
        # Find config file
        config_file = Path(self.config) if self.config.endswith((".yml", ".yaml")) and Path(self.config).is_file() else _find_config_file(self.config)
        config_file = config_file.absolute()
        with open(config_file, "r") as file:
            config: dict[str, Any] = yaml.safe_load(file)
        config_name = self.__generate_config_name(config_file)
        print(f"🔵 PREFIX: {config_name}")
        # Kill previous runs
        os.system(f"pkill -f java -u {USERNAME} -9")
        # Setup env
        env = {
            "BUILDS": f"{EVALUATION_DIR}/builds",
            "CONFIGS": f"{EVALUATION_DIR}/configs",
            "PATH": os.environ["PATH"],
            "CONFIG": str(config_file),
            "ID_PREFIX": config_name,
        }
        os.environ.update(env)
        # Run
        cmd = self.__get_command(config, config_file, config_name)
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
