import argparse, subprocess, os
from config import * 

def MultiEntryMain(**SUB_COMMANDS):
  # Parse command line arguments
  parser = argparse.ArgumentParser(description='MMTk Development Script')
  parser.add_argument('--moma', default=DEFAULT_MOMA_MACHINE, help='Moma machine')
  subparsers = parser.add_subparsers(dest='cmd', help='Sub commands')
  for key, config in SUB_COMMANDS.items():
    config.config(subparsers.add_parser(key, help=getattr(config, 'help', '')))
  options = parser.parse_args()
  # Trigger sub task
  for key, callback in SUB_COMMANDS.items():
    if options.cmd == key:
      if not callback.action(options):
        print("💩")
      break
  else:
    parser.print_help()

def SingleEntryMain(config):
  # Parse command line arguments
  parser = argparse.ArgumentParser(description='MMTk Development Script')
  parser.add_argument('--moma', default=DEFAULT_MOMA_MACHINE, help='Moma machine')
  config.config(parser)
  options = parser.parse_args()
  config.action(options)

def shell(commands, moma=None, cwd=None, out=None, verbose=True):
  commands = commands if moma is None else ['ssh', moma + '.moma', '-t', *commands]
  stdout = None
  if out is not None:
    os.makedirs(os.path.dirname(out), exist_ok=True)
    stdout = open(out, 'w+')
  if verbose: print(f"> {' '.join(commands)}")
  result = subprocess.call(commands, cwd=cwd, stdout=stdout) == 0
  if stdout is not None:
    stdout.close()
  return result