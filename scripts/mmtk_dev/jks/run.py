#!/usr/bin/env python3

from dataclasses import dataclass
from enum import Enum
import os
import subprocess
from typing import Any, Optional, List
from mmtk_dev.constants import MMTK_DEV, MMTK_JIKESRVM, JIKESRVM, DACAPO_9_12, PROBES
from mmtk_dev.utils import ᐅᐳᐳ
from simple_parsing import field


class Profile(str, Enum):
    release = "release"
    fastdebug = "fastdebug"
    slowdebug = "slowdebug"


def do_kill():
    user = os.getlogin()
    ᐅᐳᐳ("pkill", "-f", "rvm", "-u", user, "-9")


@dataclass
class Build:
    """
    Build jikesrvm

    Example: mmtk-jks build --target RBaseBaseSemiSpace
    """

    target: str
    """Target with GC plan. e.g. RBaseBaseSemiSpace"""

    def run(self):
        ᐅᐳᐳ(
            "./bin/buildit",
            "localhost",
            self.target,
            "--use-third-party-heap=../mmtk-jikesrvm",
            "--use-third-party-build-configs=../mmtk-jikesrvm/jikesrvm/build/configs/",
            "--use-external-source=../mmtk-jikesrvm/jikesrvm/rvm/src",
            "--m32",
            "--answer-yes",
            cwd=JIKESRVM,
        )


@dataclass
class Run:
    """
    Run JikesRVM

    Example: mmtk-jks run --target RBaseBaseSemiSpace --heap 100M --bench lusearch --build
    """

    target: str
    """Target with GC plan. e.g. RBaseBaseSemiSpace"""

    heap: str
    """Heap size"""

    bench: str
    """DaCapo benchmark name"""

    # Optional run args

    iter: int = field(alias="n", default=1)
    """Number of iterations"""

    build: bool = field(alias="b", default=False, negative_prefix="--no-")
    """Build JikesRVM and MMTk before run"""

    def run(self):
        if self.build:
            build = Build(self.target)
            build.run()
        env = {}
        env["RUST_BACKTRACE"] = "1"
        env["LD_LIBRARY_PATH"] = f"dist/{self.target}_x86_64_m32-linux/"

        heap_args: List[Any] = [f"-Xms{self.heap}", f"-Xmx{self.heap}"]
        dacapo_args = ["-jar", "/usr/share/benchmarks/dacapo/dacapo-9.12-bach.jar", self.bench, "-n", f"{iter}"]

        ᐅᐳᐳ(
            f"dist/{self.target}_x86_64_m32-linux/rvm",
            *heap_args,
            *dacapo_args,
            env=env,
            cwd=JIKESRVM,
        )
