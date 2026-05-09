import os
from pathlib import Path
import subprocess
import sys
import tempfile
from typing import Any
import yaml
from ..constants import FULL_JDK_PROFILE, MMTK_DEV, EVALUATION_DIR, OPENJDK, USERNAME
from dataclasses import dataclass
from simple_parsing import field
from ..utils import ᐅᐳᐳ
from .run import JVMArgs, Run as RunJDK, Build as BuildJDK, DEFAULT_PGO_TRAINING_BENCHMARKS
import rich
import shlex

CLASS_UNLOADING = False


def err(s: str):
    rich.print(f"[bold on red]ERROR:[/] [bold red]{s}[/]")
    sys.exit(1)


def check(condition: bool, s: str):
    if not condition:
        err(s)
    return True


def warn(s: str):
    rich.print(f"[bold on yellow]WARNING:[/] [bold yellow]{s}[/]")


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

    gc: str | None
    """GC to test the build"""

    clean: bool = field(default=False, negative_prefix="--no-")
    """Clean the build directory"""

    reconfigure: bool = field(default=False, negative_prefix="--no-")
    """reconfigure the build directory"""

    allow_dirty: bool = field(default=False, negative_prefix="--no-")
    """Allow dirty workspace"""

    def __validate_repos(self):
        __err = err if not self.allow_dirty else warn

        if os.system(f"cd {MMTK_DEV} && git diff --quiet") != 0:
            __err("Current mmtk-dev workspace is dirty!")
        if os.system(f"cd {MMTK_DEV}/mmtk-core && git diff --quiet") != 0:
            __err("Current mmtk-core repo is dirty!")
        if os.system(f"cd {MMTK_DEV}/mmtk-openjdk && git diff --quiet") != 0:
            __err("Current mmtk-openjdk repo is dirty!")
        if os.system(f"cd {MMTK_DEV}/openjdk && git diff --quiet") != 0:
            __err("Current openjdk repo is dirty!")

    def __is_at_commit(self, repo: Path, commit: str) -> bool:
        return os.system(f"cd {repo} && git diff --quiet {commit}") == 0

    def __checkout(self, repo: Path, commit: str):
        if self.__is_at_commit(repo, commit):
            return
        if os.system(f"cd {repo} && git checkout {commit} --force") != 0:
            err(f"Failed to checkout {commit} for repo {repo.name}")

    def __build_one(self, runtime_name: str, home: str, features: str | None, exploded: bool, test_command: str | None, pgo: bool | str, build_gc: str | None):
        try:
            if test_command is None:
                pgo_enabled = pgo if isinstance(pgo, bool) else True
                pgo_benchmarks = pgo if isinstance(pgo, str) else ",".join(DEFAULT_PGO_TRAINING_BENCHMARKS)
                if not CLASS_UNLOADING:
                    jvm_args = JVMArgs(class_unloading=False)
                else:
                    jvm_args = JVMArgs()
                run = RunJDK(gc=self.gc or build_gc or "Immix", bench="fop", heap="500M", build=True, release=True, features=features, config=self.reconfigure or self.clean, clean=self.clean, bundle=not exploded, exploded=exploded, pgo=pgo_enabled, pgo_benchmarks=pgo_benchmarks, jvm=jvm_args)
                # run = RunJDK(gc=self.gc, bench="fop", heap="500M", build=True, release=True, features=features, config=self.reconfigure or self.clean, clean=self.clean, bundle=not exploded, exploded=exploded, jvm=JVMArgs(compressed_oops=False))
                run.run()
            else:
                check(not pgo, "PGO is not supported with custom test command")
                build = BuildJDK(release=True, features=features, config=self.reconfigure or self.clean, clean=self.clean, bundle=not exploded, exploded=exploded)
                build.run()
                result = os.system(test_command)
                check(result == 0, f"Test command failed with exit code {result}")

            jdk_home = Path(home).resolve()
            if exploded:
                self.__copy_jdk_bundle_exploded(jdk_home)
            else:
                self.__copy_jdk_bundle(jdk_home)
        except BaseException as e:
            err(f"Failed to build `runtimes.{runtime_name}`: [not bold]{e}[/]")

    def __copy_jdk_bundle_exploded(self, home: Path):
        home.parent.mkdir(parents=True, exist_ok=True)
        # Delete previous builds
        ᐅᐳᐳ("rm", "-rf", home)
        # Copy exploded jdk folder
        ᐅᐳᐳ("cp", "-r", OPENJDK / "build" / FULL_JDK_PROFILE("release"), home)

    def __copy_jdk_bundle(self, home: Path):
        home.parent.mkdir(parents=True, exist_ok=True)
        # Get bundle file
        bundle = subprocess.check_output(["bash", "-c", f"ls {OPENJDK}/build/{FULL_JDK_PROFILE('release')}/bundles/*.tar.gz | grep -v -e symbols -e demos"], cwd=MMTK_DEV).decode("utf-8").strip()
        # Delete previous builds
        ᐅᐳᐳ("rm", "-rf", home)
        home.mkdir(parents=True, exist_ok=True)
        # Copy bundle file
        temp_file = home.parent / f"jdk.tar.gz"
        ᐅᐳᐳ("rm", "-f", temp_file)
        ᐅᐳᐳ("cp", bundle, temp_file)
        # Extract and remove bundle file
        ᐅᐳᐳ("tar", "-xf", temp_file, "--strip-components=1", "-C", home)
        ᐅᐳᐳ("rm", "-f", temp_file)

    def __check_builds(self, runtimes: Any):
        builds: set[str] = set()
        for runtime_name, runtime in runtimes.items():
            home: str | None = runtime.get("home")
            check(home is not None, f"`runtimes.{runtime_name}.home` is not defined")
            check(home not in builds, f"Duplicated value for `runtimes.{runtime_name}.home`: [not bold]{home}[/]")
            assert home
            builds.add(home)
            exploded: bool = runtime.get("exploded", False)
            if exploded:
                check(home.endswith("/jdk"), f"Invalid value for `runtimes.{runtime_name}.home`: [not bold]{home} (must end with /jdk for exploded builds)[/]")

    def run(self):
        os.environ["BUILDS"] = f"{EVALUATION_DIR}/builds"
        self.__validate_repos()
        config_file = _find_config_file(self.config)
        with open(config_file, "r") as file:
            doc = yaml.safe_load(file)
            self.__check_builds(doc["runtimes"])
            build_gc = doc.get("build_gc")
            # if build_gc is not None:
            rich.print(f"[bold on green]BUILD GC: {build_gc}[/]\n")
            for runtime_name, runtime in doc["runtimes"].items():
                cwd = OPENJDK / "build" / FULL_JDK_PROFILE("release")
                if cwd.exists():
                    ᐅᐳᐳ("rm", "-rf", cwd)
                assert "commits" in runtime, f"❌ `runtimes.{runtime_name}.commits` is not defined"
                commits = runtime["commits"]
                if commits is None:
                    rich.print(f"[bold green][{runtime_name}]: Skipping build\n[/]")
                    continue
                features = runtime.get("features")
                exploded = runtime.get("exploded", False)
                test_command = runtime.get("test-command")
                pgo = runtime.get("pgo", False)
                # checkout commits
                rich.print(f"[bold on green]BUILD {runtime_name}[/]")
                rich.print(f"[bold green]CHECKOUT[/]: [green]mmtk-core@{commits['mmtk-core']} mmtk-openjdk@{commits['mmtk-openjdk']} openjdk@{commits['openjdk']}[/]")
                if features:
                    rich.print(f"[bold green]RUST FEATURES[/]: [green]{features}[/]")
                print()
                self.__checkout(MMTK_DEV / "mmtk-core", commits["mmtk-core"])
                self.__checkout(MMTK_DEV / "mmtk-openjdk", commits["mmtk-openjdk"])
                self.__checkout(MMTK_DEV / "openjdk", commits["openjdk"])
                print()
                # build and copy target
                features = runtime.get("features")
                home: str = os.path.expandvars(runtime["home"])
                if home.endswith("/"):
                    home = home[:-1]
                self.__build_one(runtime_name=runtime_name, home=home, features=features, exploded=exploded, test_command=test_command, pgo=pgo, build_gc=build_gc)
                assert os.path.isfile(f"{home}/release"), f"❌ Failed to build `runtimes.{runtime_name}`: {home}/release does not exist"
                rich.print(f"[bold on green]BUILD COMPLETED:  {runtime_name}[/]\n\n\n")


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

    def __run_uv_sync(self):
        MMTK_DEV_REL = str(MMTK_DEV).replace(os.path.expanduser("~") + "/", "")
        cmd = ["ssh", f"{self.remote_user}@{self.remote}", f"cd {MMTK_DEV_REL} && uv sync --locked"]
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
        self.__rsync(f"/home/{USERNAME}/./{MMTK_DEV_REL}/evaluation/schedule-bear.sh", dst)
        self.__rsync(f"/home/{USERNAME}/./{MMTK_DEV_REL}/evaluation/schedule-boar.sh", dst)
        self.__rsync(f"/home/{USERNAME}/./{MMTK_DEV_REL}/evaluation/schedule-mink.sh", dst)
        self.__rsync(f"/home/{USERNAME}/./{MMTK_DEV_REL}/uv.lock", dst)
        self.__rsync(f"/home/{USERNAME}/./{MMTK_DEV_REL}/pyproject.toml", dst)
        self.__rsync(f"/home/{USERNAME}/./{MMTK_DEV_REL}/scripts/mmtk_dev", dst)
        self.__rsync(f"/home/{USERNAME}/./{MMTK_DEV_REL}/README.md", dst)
        self.__run_uv_sync()


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

    anu: bool = field(default=True, negative_prefix="--no-")
    """Rsycn results to squirrel.moma"""

    invocations: int | None = None

    workdir: Path | None = None

    def __get_hfac_args_list(self, config: dict[str, Any]) -> list[list[str]]:
        hfac_list: list[str] | None = None
        if self.hfac is None:
            cfg_hac = config.get("hfac") or config.get("overrides", {}).get("hfac")
            if cfg_hac is None:
                sys.exit(f"❌ `hfac` is not defined in both command line and config file")
            if isinstance(cfg_hac, str):
                hfac_list = [cfg_hac.strip().lower()]
            elif isinstance(cfg_hac, list):
                hfac_list = [x.strip().lower() for x in cfg_hac]
            else:
                sys.exit(f"❌ Invalid hfac: {config['hfac']}")
        else:
            hfac_list = [self.hfac.strip().lower()]

        results = []
        for hfac in hfac_list:
            if hfac == "1x":
                result = ["12", "0"]
            elif hfac == "1.3x":
                result = ["32", "7"]
            elif hfac == "1.4x":
                result = ["12", "3"]
            elif hfac == "1.5x":
                result = ["12", "4"]
            elif hfac == "2x":
                result = ["12", "7"]
            elif hfac == "3x":
                result = ["12", "12"]
            elif "-" in hfac:
                try:
                    result = [f"{int(x)}" for x in hfac.split("-")]
                except ValueError:
                    sys.exit(f"❌ Invalid hfac args `{hfac}`")
            else:
                sys.exit(f"❌ Invalid hfac args `{hfac}`")
            results.append(result)
        return results

    def __get_commands(self, config: dict[str, Any], config_file: Path, config_name: str) -> list[list[str]]:
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
            commands = [cmd]
        else:
            # Get heap args
            commands = []
            for hfac_args in self.__get_hfac_args_list(config):
                # Run
                os.system(f"pkill -f java -u {USERNAME} -9")
                workdir_args = [] if self.workdir is None else ["--workdir", str(self.workdir)]
                if self.invocations is not None:
                    rich.print(f"[bold blue]INVOCATIONS:[/] {self.invocations}")
                    inv = ["--invocations", f"{self.invocations}"]
                else:
                    inv = []
                bin = config.get("bin", "running")
                cmd: list[str] = [bin, "runbms", *workdir_args, "-p", config_name, *inv, "./evaluation/results/log", str(config_file), *hfac_args]
                commands.append(cmd)
        return commands

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
        rich.print(f"[bold blue]PREFIX:[/] {config_name}")
        # Kill previous runs
        os.system(f"pkill -f java -u {USERNAME} -9")
        # Setup env
        env = {
            "BUILDS": f"{EVALUATION_DIR}/builds",
            "CONFIGS": f"{EVALUATION_DIR}/configs",
            "PATH": os.environ["PATH"],
            "CONFIG": str(config_file),
            "ID_PREFIX": config_name,
            "__ANU": "-anu" if self.anu else "",  # a special flag to enable rsync results to squirrel.moma
        }
        os.environ.update(env)
        # Clear log file
        if self.log.exists():
            self.log.unlink(missing_ok=True)
        # Run
        for cmd in self.__get_commands(config, config_file, config_name):
            rich.print(f'[bold blue]RUN:[/] [bright_black]{" ".join(cmd)}')
            rich.print(f"[bold blue]LOG:[/] {self.log}")
            rich.print(f'[bold blue]BUILDS:[/] {env["BUILDS"]}')
            with open(self.log, "a") as logfile:
                subprocess.check_call(cmd, stdout=logfile, stderr=logfile, cwd=MMTK_DEV, env=env)
        rich.print(f"[bold on green]Benchmark completed.[/]")


@dataclass
class Minheap:
    """
    Start a minheap run

    Example: mmtk-jdk bench minheap --config minheap
    """

    config: str
    """Running config name or path to a running config file"""

    out: Path = MMTK_DEV / "_minheap.yaml"
    """Output file"""

    log: Path = MMTK_DEV / "running.log"
    """Log file"""

    def run(self):
        # Find config file
        config_file = Path(self.config) if self.config.endswith((".yml", ".yaml")) and Path(self.config).is_file() else _find_config_file(self.config)
        config_file = config_file.absolute()
        with open(config_file, "r") as file:
            config: dict[str, Any] = yaml.safe_load(file)
        # Setup env
        env = {
            "BUILDS": f"{EVALUATION_DIR}/builds",
            "CONFIGS": f"{EVALUATION_DIR}/configs",
            "PATH": os.environ["PATH"],
            "CONFIG": str(config_file),
            "__ANU": "",  # a special flag to enable rsync results to squirrel.moma
        }
        os.environ.update(env)
        # Run
        bin = config.get("bin", "running")
        cmd: list[str] = [bin, "minheap", str(config_file), str(self.out)]
        rich.print(f'[bold blue]RUN:[/] {" ".join(cmd)}')
        rich.print(f"[bold blue]OUT:[/] {self.out}")
        rich.print(f'[bold blue]BUILDS:[/] {env["BUILDS"]}')
        with open(self.log, "w+") as logfile:
            subprocess.check_call(cmd, stdout=logfile, stderr=logfile, cwd=MMTK_DEV, env=env)
        rich.print(f"[bold on green]Minheap completed.[/]")


@dataclass
class Status:
    """
    show status of the running benchmark

    Example: mmtk-jdk bench status --remote bear.moma
    """

    remote: str
    """Remote machine name"""

    remote_user: str = USERNAME
    """Remote user name"""

    def __scp(self, src: str, dst: str):
        cmd = ["scp", "-q", src, dst]
        try:
            subprocess.check_call(cmd, cwd=MMTK_DEV)
        except subprocess.CalledProcessError:
            sys.exit(f'❌ {" ".join(cmd)}')

    def run(self):
        src = f"{self.remote_user}@{self.remote}:/home/{self.remote_user}/MMTk-Dev/running.log"
        with tempfile.NamedTemporaryFile(prefix="running", suffix=".log") as tmp:
            self.__scp(src, tmp.name)
            os.system(f"cat {tmp.name}")


@dataclass
class Bench:
    """
    Benchmarking utils

    Sub-commands:
      build       build jdk(s) for benchmarking
      rsync       rsync builds and benchmark configs to a remote machine
      run         run benchmark
    """

    command: Build | Rsync | Run | Status | Minheap
    """Sub-commands"""

    def run(self):
        self.command.run()
