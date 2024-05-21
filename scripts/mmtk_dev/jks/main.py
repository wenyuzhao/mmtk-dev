import sys
from mmtk_dev.utils import MMTkDevArgumentParser
from simple_parsing.helpers.fields import subparsers
from dataclasses import dataclass
from simple_parsing.wrappers.field_wrapper import DashVariant
from .run import Build, Run


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
        }
    )
    """Sub-commands"""

    def run(self):
        self.command.run()


def main():
    parser = MMTkDevArgumentParser(add_option_string_dash_variants=DashVariant.DASH)
    parser.add_arguments(Command, dest="command")
    args = parser.parse_args(args=MMTkDevArgumentParser.fix_args(sys.argv[1:], "rbx"))
    args.command.run()
