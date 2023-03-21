#!/usr/bin/env python3

import os
import os.path
from typing import *
import subprocess
import typer
import sys

LOCAL_USER = os.getlogin()

USERNAME = os.getlogin()
EVALUATION_DIR = os.path.dirname(os.path.realpath(__file__))
MMTK_DEV = os.path.dirname(EVALUATION_DIR)

app = typer.Typer()

def rsync(src: str, dst: str):
    cmd = ['rsync', '-azR', '--no-i-r', '-h', '--info=progress2', src, dst]
    print(f'🔵 {" ".join(cmd)}')
    try:
        subprocess.check_call(cmd, cwd=MMTK_DEV)
    except subprocess.CalledProcessError:
        sys.exit(f'❌ {" ".join(cmd)}')

@app.command()
def main(
    remote: str = typer.Option(..., help='Remote machine name'),
    remote_user: str = typer.Option(LOCAL_USER, help='Remote user name'),
):
    '''
        Example: ./evaluation/rsync.py --remote boar.moma
    '''
    dst = f'{remote}:/home/{remote_user}'
    MMTK_DEV_REL = MMTK_DEV.replace(os.path.expanduser('~') + '/', '')
    rsync(f'/home/{LOCAL_USER}/./{MMTK_DEV_REL}/evaluation/configs', dst)
    rsync(f'/home/{LOCAL_USER}/./{MMTK_DEV_REL}/evaluation/advice', dst)
    rsync(f'/home/{LOCAL_USER}/./{MMTK_DEV_REL}/evaluation/probes', dst)
    rsync(f'/home/{LOCAL_USER}/./{MMTK_DEV_REL}/evaluation/builds', dst)
    rsync(f'/home/{LOCAL_USER}/./{MMTK_DEV_REL}/evaluation/run.py', dst)
    rsync(f'/home/{LOCAL_USER}/./{MMTK_DEV_REL}/evaluation/rsync.py', dst)

if __name__ == '__main__':
    app(prog_name='evaluation/rsync.py')