import inspect
import pathlib
import sys
from typing import Any
from simple_parsing.helpers.fields import subparsers
from dataclasses import dataclass
from simple_parsing import ArgumentGenerationMode, ArgumentParser, NestedMode
from simple_parsing.wrappers.field_wrapper import DashVariant
from .run import Build, Run, Clean
from .bench import Bench


@dataclass
class Command:
    """
    Commands for build and run OpenJDK with MMTk

    Example: mmtk-jdk r --gc LXR --heap 100M --bench lusearch --build

    Sub-commands:
      build,b     build OpenJDK with MMTk
      run,r       run OpenJDK with MMTk
      bench       benchmark tools
    """

    command: Run = subparsers(
        {
            "build": Build,
            "b": Build,
            "run": Run,
            "r": Run,
            "clean": Clean,
            "bench": Bench,
        }
    )
    """Sub-commands"""

    def run(self):
        self.command.run()


_FIRST_KWARGS: Any = None


class _ArgumentParser(ArgumentParser):
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


def main():
    parser = _ArgumentParser(
        add_option_string_dash_variants=DashVariant.DASH,
        # argument_generation_mode=ArgumentGenerationMode.BOTH,
        # nested_mode=NestedMode.WITHOUT_ROOT,
    )
    parser.add_arguments(Command, dest="command")
    args = parser.parse_args(args=_ArgumentParser.fix_args(sys.argv[1:], "rbx"))
    args.command.run()
