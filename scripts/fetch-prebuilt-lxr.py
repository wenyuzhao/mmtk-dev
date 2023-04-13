#!/usr/bin/env python3

from mmtk_utils import *
import os

@app.command()
def main(date: str = option(..., help='Date e.g. 20230330')):
    '''
        Example: ./scripts/fetch-prebuilt-lxr.py --date 20230330
    '''
    if os.path.exists(f'{MMTK_DEV}/builds/lxr-{date}'):
        print(f'./builds/lxr-{date} already exists!')
        return
    ᐅᐳᐳ(['mkdir', '-p', f'builds/lxr-{date}'], cwd=MMTK_DEV)
    if not os.path.exists(f'{MMTK_DEV}/builds/jdk11-linux-x86_64-normal-server-mmtk-lxr-release-{date}.tar.gz'):
        ᐅᐳᐳ(['wget', f'https://github.com/wenyuzhao/lxr-builds/releases/download/nightly/jdk11-linux-x86_64-normal-server-mmtk-lxr-release-{date}.tar.gz'], cwd=f'{MMTK_DEV}/builds')
    ᐅᐳᐳ(['tar', 'xf', f'jdk11-linux-x86_64-normal-server-mmtk-lxr-release-{date}.tar.gz', '-C', f'lxr-{date}', '--strip-components=1'], cwd=f'{MMTK_DEV}/builds')

if __name__ == '__main__':
    app(prog_name='run-jdk')