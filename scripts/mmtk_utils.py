import click
import subprocess
import os
from typing import *
import typer
import sys

app = typer.Typer()

MMTK_DEV = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
MMTK_CORE = f'{MMTK_DEV}/mmtk-core'
BENCH_BUILDS = f'{MMTK_DEV}/evaluation/builds'
PROBES = f'{MMTK_DEV}/evaluation/probes'
if not os.path.isfile(PROBES + '/Makefile'): PROBES = None

def option(*args, **kwargs):
    return typer.Option(*args, **kwargs)

def argument(*args, **kwargs):
    return typer.Argument(*args, **kwargs)

def ᐅᐳᐳ(cmd: List[str], cwd: str = MMTK_DEV, env: Optional[Dict[str, str]] = None):
    env = ' '.join([ f'{k}={v}' for k, v in env.items() ])
    cmd = ' '.join(cmd)
    print(f'🔵 {env} {cmd}')
    result = os.system(f'cd {cwd} && {env} {cmd}')
    if result != 0:
        sys.exit(f'❌ {cmd}')   

