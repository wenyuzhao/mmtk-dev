import os
from typing import Any, Optional, Dict, List
import typer
import sys

app = typer.Typer()

MMTK_DEV = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
MMTK_CORE = f"{MMTK_DEV}/mmtk-core"
BENCH_BUILDS = f"{MMTK_DEV}/evaluation/builds"
PROBES = f"{MMTK_DEV}/evaluation/probes" if os.path.isfile(f"{MMTK_DEV}/evaluation/probes/probes.jar") else None


def option(*args: Any, **kwargs: Any) -> Any:
    return typer.Option(*args, **kwargs)


def argument(*args: Any, **kwargs: Any) -> Any:
    return typer.Argument(*args, **kwargs)


def ᐅᐳᐳ(cmd: List[str], cwd: str = MMTK_DEV, env: Optional[Dict[str, str]] = None) -> Any:
    if env is None:
        env = {}
    env_s = " ".join([f"{k}={v}" for k, v in env.items()])
    cmd_s = " ".join(cmd)
    msg = ""
    if env_s != "":
        msg += f"{env_s} "
    msg += cmd_s
    print(f"🔵 {msg}")
    result = os.system(f"cd {cwd} && {env_s} {cmd_s}")
    if result != 0:
        sys.exit(f"❌ {cmd_s}")
