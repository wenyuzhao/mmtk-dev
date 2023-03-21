#!/usr/bin/env python3
from mmtk_utils import *
import argparse, os


MMTK_DEV = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
LOCAL_USER = os.getlogin()


def parse_args():
    parser = argparse.ArgumentParser(description=f'Benchmark files remote sync.\n\nExample: ./{os.path.basename(__file__)} --machine=deer.moma', add_help=False, formatter_class=argparse.RawTextHelpFormatter)
    # Required arguments
    required = parser.add_argument_group('required arguments')
    required.add_argument('--machine', type=str, required=True, help="Remote machine")
    # Optional arguments
    optional = parser.add_argument_group('optional arguments')
    optional.add_argument('--user', type=str, default=LOCAL_USER, help=f"Remote machine username. Default to {LOCAL_USER}")
    optional.add_argument('-h', '--help', action='help', default=argparse.SUPPRESS, help='Show this help message and exit')
    return parser.parse_args()

def rsync_files(machine: str, user: str):
    rsync = lambda src, dst: ᐅᐳᐳ(['rsync', '-azR', '--no-i-r', '-h', '--info=progress2', src, dst], cwd=MMTK_DEV)
    dst = f'{machine}:/home/{user}'
    rsync("~/./MMTk-Dev/evaluation/configs", dst)
    rsync("~/./MMTk-Dev/evaluation/advice", dst)
    rsync("~/./MMTk-Dev/evaluation/probes", dst)
    rsync("~/./MMTk-Dev/evaluation/builds", dst)

args = parse_args()

rsync_files(args.machine, args.user)
