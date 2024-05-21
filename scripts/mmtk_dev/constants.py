import os
from pathlib import Path
import sys

MMTK_DEV = Path(__file__).parent.parent.parent

OPENJDK = MMTK_DEV / "openjdk"

MMTK_CORE = MMTK_DEV / "mmtk-core"

MMTK_OPENJDK = MMTK_DEV / "mmtk-openjdk"

MMTK_JIKESRVM = MMTK_DEV / "mmtk-jikesrvm"

JIKESRVM = MMTK_DEV / "jikesrvm"

DACAPO_ROOT = Path("/usr/share/benchmarks/dacapo")


def __find_dacapo_chopin():
    possible_paths = [
        # Chopin stable release
        DACAPO_ROOT / "dacapo-23.11-chopin.jar",
        # Chopin RC releases
        *(DACAPO_ROOT / f"dacapo-23.9-RC{v}-chopin.jar" for v in reversed(range(1, 10))),
        # Chopin temporary releases
        *(DACAPO_ROOT / f"dacapo-evaluation-git-{v}.jar" for v in ["04132797", "6e411f33", "b00bfa9"]),
    ]
    for path in possible_paths:
        if path.is_file():
            return path
    sys.exit(f"❌ Could not find a dacapo jar file")


DACAPO_CHOPIN = __find_dacapo_chopin()

DACAPO_9_12 = DACAPO_ROOT / "dacapo-9.12-bach.jar"


PROBES = (MMTK_DEV / "evaluation" / "probes") if (MMTK_DEV / "evaluation" / "probes" / "probes.jar").is_file() else None

EVALUATION_DIR = MMTK_DEV / "evaluation"

try:
    USERNAME = os.getlogin()
except BaseException:
    USERNAME = os.environ["USER"]
