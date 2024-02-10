#!/usr/bin/env python3

import os
import os.path
from typing import Optional
import subprocess
import typer
import sys
import yaml
import re


try:
    USERNAME = os.getlogin()
except BaseException:
    USERNAME = os.environ["USER"]
EVALUATION_DIR = os.path.dirname(os.path.realpath(__file__))
MMTK_DEV = os.path.dirname(EVALUATION_DIR)


os.environ["BUILDS"] = f"{EVALUATION_DIR}/builds"

app = typer.Typer()


def do_rsync(src: str, dst: str):
    cmd = ["rsync", "-azR", "--no-i-r", "-h", "--info=progress2", src, dst]
    print(f'🔵 {" ".join(cmd)}')
    try:
        subprocess.check_call(cmd, cwd=MMTK_DEV)
    except subprocess.CalledProcessError:
        sys.exit(f'❌ {" ".join(cmd)}')


def find_config_file(config: str):
    # Find config file
    config_file = None
    if os.path.isfile(f"{EVALUATION_DIR}/configs/{config}.yml"):
        config_file = f"{EVALUATION_DIR}/configs/{config}.yml"
    elif os.path.isfile(f"{EVALUATION_DIR}/configs/{config}.yaml"):
        config_file = f"{EVALUATION_DIR}/configs/{config}.yaml"
    elif os.path.isfile(f"{EVALUATION_DIR}/configs/{config}/config.yml"):
        config_file = f"{EVALUATION_DIR}/configs/{config}/config.yml"
    elif os.path.isfile(f"{EVALUATION_DIR}/configs/{config}/config.yaml"):
        config_file = f"{EVALUATION_DIR}/configs/{config}/config.yaml"
    if config_file is None:
        sys.exit(f"❌ Config `{config}` not found!")
    return config_file


def build_one(runtime_name: str, build_name: str, features: Optional[str], gc: str, config: bool):
    features_flag = ""
    if features is not None:
        features_flag = f'--features="{features}"'
    config_flag = ""
    if config:
        config_flag = "--config"
    bench = "fop"
    print(f"🔵 run-jdk --gc={gc} --bench={bench} --heap=500M --build --release --cp-bench={build_name} --cp-bench-no-commit-hash {features_flag} {config_flag}")
    ret = os.system(f"{MMTK_DEV}/run-jdk --gc={gc} --bench={bench} --heap=500M --build --release --cp-bench={build_name} --cp-bench-no-commit-hash {features_flag} {config_flag}")
    if ret != 0:
        sys.exit(f"❌ Failed to build `runtimes.{runtime_name}`!")


def checkout(name: str, repo: str, commit: str):
    if os.system(f"cd {repo} && git checkout {commit}") != 0:
        sys.exit(f"❌ Failed to checkout {commit} for repo {name}")


def get_current_commits():
    mmtk_core_commit = subprocess.check_output(["git", "rev-parse", "--short", "HEAD"], cwd=f"{MMTK_DEV}/mmtk-core").decode("utf-8").strip()
    mmtk_openjdk_commit = subprocess.check_output(["git", "rev-parse", "--short", "HEAD"], cwd=f"{MMTK_DEV}/mmtk-openjdk").decode("utf-8").strip()
    openjdk_commit = subprocess.check_output(["git", "rev-parse", "--short", "HEAD"], cwd=f"{MMTK_DEV}/openjdk").decode("utf-8").strip()
    return (mmtk_core_commit, mmtk_openjdk_commit, openjdk_commit)


def is_at_commit(repo: str, commit: str) -> bool:
    return os.system(f"cd {repo} && git diff --quiet {commit}") == 0


def validate_config(config_file: str):
    with open(config_file, "r") as file:
        doc = yaml.safe_load(file)
        # validate
        missing_commits = False
        for runtime_name in doc["runtimes"]:
            commits = doc["runtimes"][runtime_name].get("commits", {})
            if commits is None or ("mmtk-core" not in commits) or ("mmtk-openjdk" not in commits) or ("openjdk" not in commits):
                if "mmtk-core" not in commits:
                    print(f"❌ runtimes.{runtime_name} has no `mmtk-core` commit specified!")
                if "mmtk-openjdk" not in commits:
                    print(f"❌ runtimes.{runtime_name} has no `mmtk-openjdk` commit specified!")
                if "openjdk" not in commits:
                    print(f"❌ runtimes.{runtime_name} has no `openjdk` commit specified!")
                missing_commits = True
        if missing_commits:
            (mmtk_core_commit, mmtk_openjdk_commit, openjdk_commit) = get_current_commits()
            print("Current commits:")
            print(f"    mmtk-core: {mmtk_core_commit}")
            print(f"    mmtk-openjdk: {mmtk_openjdk_commit}")
            print(f"    openjdk: {openjdk_commit}")
            sys.exit(-1)


def validate_repos():
    if os.system(f"cd {MMTK_DEV} && git diff --quiet") != 0:
        sys.exit(f"❌ Current mmtk-dev workspace is dirty!")
    if os.system(f"cd {MMTK_DEV}/mmtk-core && git diff --quiet") != 0:
        sys.exit(f"❌ Current mmtk-core repo is dirty!")
    if os.system(f"cd {MMTK_DEV}/mmtk-openjdk && git diff --quiet") != 0:
        sys.exit(f"❌ Current mmtk-openjdk repo is dirty!")
    if os.system(f"cd {MMTK_DEV}/openjdk && git diff --quiet") != 0:
        sys.exit(f"❌ Current openjdk repo is dirty!")


@app.command()
def build(
    config: str = typer.Option(..., help="Running config name"),
    gc: str = typer.Option("Immix", help="GC to test the build"),
):
    """
    Example: ./evaluation/manager.py build --config=lxr-xput
    """
    validate_repos()
    # Parse config file, find and compile each build
    config_file = find_config_file(config)
    validate_config(config_file)
    with open(config_file, "r") as file:
        doc = yaml.safe_load(file)
        for runtime_name in doc["runtimes"]:
            commits = doc["runtimes"][runtime_name]["commits"]
            features = doc["runtimes"][runtime_name].get("features")
            # checkout commits
            print(f"🟢 [{runtime_name}]: mmtk-core@{commits['mmtk-core']} mmtk-openjdk@{commits['mmtk-openjdk']} openjdk@{commits['openjdk']} features={features}")
            if not is_at_commit(f"{MMTK_DEV}/mmtk-core", commits["mmtk-core"]):
                checkout("mmtk-core", f"{MMTK_DEV}/mmtk-core", commits["mmtk-core"])
            if not is_at_commit(f"{MMTK_DEV}/mmtk-openjdk", commits["mmtk-openjdk"]):
                checkout("mmtk-openjdk", f"{MMTK_DEV}/mmtk-openjdk", commits["mmtk-openjdk"])
            if not is_at_commit(f"{MMTK_DEV}/openjdk", commits["openjdk"]):
                checkout("openjdk", f"{MMTK_DEV}/openjdk", commits["openjdk"])
            reconfig_jdk = doc["runtimes"][runtime_name].get("reconfig-jdk", False)
            # build and copy target
            features = doc["runtimes"][runtime_name].get("features")
            home: str = os.path.expandvars(doc["runtimes"][runtime_name]["home"])
            if home.endswith("/"):
                home = home[:-1]
            build_name = os.path.split(os.path.split(home)[0])[1]
            build_one(runtime_name, build_name, features, gc, config=reconfig_jdk)
            assert os.path.isfile(f"{home}/release"), f"❌ Failed to build `runtimes.{runtime_name}`"
            print(f"✅ [{runtime_name}]: Build successful")
            print()
            print()
            print()


@app.command()
def rsync(
    remote: str = typer.Option(..., help="Remote machine name"),
    remote_user: str = typer.Option(USERNAME, help="Remote user name"),
):
    """
    Example: ./evaluation/manager.py rsync --remote boar.moma
    """
    dst = f"{remote}:/home/{remote_user}"
    MMTK_DEV_REL = MMTK_DEV.replace(os.path.expanduser("~") + "/", "")
    do_rsync(f"/home/{USERNAME}/./{MMTK_DEV_REL}/evaluation/configs", dst)
    do_rsync(f"/home/{USERNAME}/./{MMTK_DEV_REL}/evaluation/advice", dst)
    do_rsync(f"/home/{USERNAME}/./{MMTK_DEV_REL}/evaluation/probes", dst)
    do_rsync(f"/home/{USERNAME}/./{MMTK_DEV_REL}/evaluation/builds", dst)
    do_rsync(f"/home/{USERNAME}/./{MMTK_DEV_REL}/evaluation/manager", dst)
    do_rsync(f"/home/{USERNAME}/./{MMTK_DEV_REL}/evaluation/manager.py", dst)
    do_rsync(f"/home/{USERNAME}/./{MMTK_DEV_REL}/poetry.lock", dst)
    do_rsync(f"/home/{USERNAME}/./{MMTK_DEV_REL}/pyproject.toml", dst)


@app.command()
def run(
    config: str = typer.Option(..., help="Running config name"),
    hfac: str = typer.Option(..., help='Heap factor. e.g. 2x or "12 1 3 4"'),
    config_file: Optional[str] = typer.Option(None, help="Path to running config file"),
    log: str = typer.Option(f"{MMTK_DEV}/running.log", help="STDOUT file"),
    workdir: Optional[str] = typer.Option(None, help="workdir"),
):
    """
    Example: ./evaluation/manager.py run --config=lxr-xput --hfac=2x
    """
    # Find config file
    config_file = find_config_file(config)

    # Get heap args
    hfac = hfac.strip().lower()
    hfac_args = []
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

    workdir_args = [] if workdir is None else ["--workdir", workdir]
    cmd = ["running", "runbms", *workdir_args, "-p", config, "./evaluation/results/log", config_file, *hfac_args]
    env = {"BUILDS": f"{EVALUATION_DIR}/builds", "PATH": os.environ["PATH"]}
    print(f'🔵 RUN: {" ".join(cmd)}')
    print(f"🔵 LOG: {log}")
    print(f'🔵 BUILDS: {env["BUILDS"]}')
    with open(log, "w") as logfile:
        subprocess.check_call(cmd, stdout=logfile, stderr=logfile, cwd=MMTK_DEV, env=env)


if __name__ == "__main__":
    app(prog_name="evaluation/manager.py")
