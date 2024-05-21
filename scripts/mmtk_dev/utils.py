import os
from typing import Any, Optional, Dict
import sys
from simple_parsing import ArgumentParser
import inspect
import pathlib
from .constants import MMTK_DEV


def ᐅᐳᐳ(prog: str | os.PathLike, *args: str | os.PathLike | None, cwd: str | os.PathLike = MMTK_DEV, env: Optional[Dict[str, str]] = None) -> Any:
    "Run a command line argument"
    if env is None:
        env = {}
    cmd = [str(prog), *(str(a) for a in args if a is not None)]
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


_FIRST_KWARGS: Any = None


class MMTkDevArgumentParser(ArgumentParser):
    def __init__(self, *args, **kwargs):
        global _FIRST_KWARGS
        if _FIRST_KWARGS is None:
            _FIRST_KWARGS = kwargs

        # only enforce FIRST_KWARGS when called by argparse
        caller = inspect.stack()[1]
        caller_path = pathlib.Path(caller.filename)
        if caller_path.match("*lib/**/argparse.py"):
            super().__init__(*args, **_FIRST_KWARGS, **kwargs)
        else:
            super().__init__(*args, **kwargs)

    @staticmethod
    def fix_args(args: list[str], single_char_flags: str):
        single_char_flags_set: set[str] = set(c for c in single_char_flags.strip())
        processed_args = []
        for a in args:
            if a.startswith("-") and not a.startswith("--") and len(a) > 1:
                if all(c in single_char_flags_set for c in a[1:]):
                    for c in a[1:]:
                        processed_args.append(f"-{c}")
                else:
                    processed_args.append(a)
            else:
                processed_args.append(a)
        return processed_args
