#!/usr/bin/env python3

import os
import os.path
from typing import *
import subprocess
import typer
import sys



USERNAME = os.getlogin()
EVALUATION_DIR = os.path.dirname(os.path.realpath(__file__))
MMTK_DEV = os.path.dirname(EVALUATION_DIR)

app = typer.Typer()

@app.command()
def main(
    config: str = typer.Option(..., help='Running config name'),
    hfac: str = typer.Option(..., help='Heap factor. e.g. 2x or "12 1 3 4"'),
    config_file: Optional[str] = typer.Option(None, help='Path to running config file'),
    log: str = typer.Option(f'{MMTK_DEV}/running.log', help='STDOUT file'),
):
    '''
        Example: ./run.py --config=lxr-input --hfac=1x
    '''
    # Find config file
    print(f'{EVALUATION_DIR}/configs/{config}.yml')
    if os.path.isfile(f'{EVALUATION_DIR}/configs/{config}/config.yml'):
        config_file = f'{EVALUATION_DIR}/configs/{config}/config.yml'
    elif os.path.isfile(f'{EVALUATION_DIR}/configs/{config}/config.yaml'):
        config_file = f'{EVALUATION_DIR}/configs/{config}/config.yaml'
    elif os.path.isfile(f'{EVALUATION_DIR}/configs/{config}.yml'):
        config_file = f'{EVALUATION_DIR}/configs/{config}.yml'
    elif os.path.isfile(f'{EVALUATION_DIR}/configs/{config}.yaml'):
        config_file = f'{EVALUATION_DIR}/configs/{config}.yaml'
    if config_file is None:
        sys.exit(f'❌ Config `{config}` not found!')

    # Get heap args
    hfac = hfac.strip().lower()
    hfac_args = []
    if hfac == '1x':
        hfac_args = ['12', '0']
    elif hfac == '2x':
        hfac_args = ['12', '7']
    elif hfac == '3x':
        hfac_args = ['12', '12']
    elif ' ' in hfac:
        try:
            hfac_args = [ f'{int(x)}' for x in hfac.split(' ')]
        except ValueError:
            sys.exit(f'❌ Invalid hfac args `{hfac}`')
    else:
        sys.exit(f'❌ Invalid hfac args `{hfac}`')
    
    # Run
    os.system(f'pkill -f java -u {USERNAME} -9')

    cmd = ['running', 'runbms', '-p', config, './evaluation/results/log', config_file, *hfac_args]
    print(f'🔵 RUN: {" ".join(cmd)}')
    print(f'🔵 LOG: {log}')
    with open(log, 'w') as log:
        subprocess.check_call(cmd, stdout=log, stderr=log, cwd=MMTK_DEV)

if __name__ == '__main__':
    app(prog_name='evaluation/run.py')