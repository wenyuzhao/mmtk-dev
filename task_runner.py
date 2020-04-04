import os
import subprocess
import sys
from inspect import signature, Parameter


DEV_DIR = os.path.dirname(os.path.realpath(__file__))
LOG_DIR = DEV_DIR + '/logs'
PIPE = subprocess.PIPE

def die(message: str = None):
    error_messages = []
    if CURRENT_TASK is not None:
        error_messages.append(f'Task `{CURRENT_TASK.__name__}` at ./{CURRENT_TASK.__code__.co_filename}:{CURRENT_TASK.__code__.co_firstlineno} failed.')
    if CURRENT_COMMAND is not None:
        error_messages.append(f'Failed at command `{CURRENT_COMMAND}`.')
    if message is not None:
        error_messages.append(f'Reason: {message}')
    max_len = max(len(s) for s in error_messages)
    max_len = 80 if max_len > 80 else max_len
    print(file=sys.stderr)
    print('-' * max_len, file=sys.stderr)
    for s in error_messages: print(s, file=sys.stderr)
    print('-' * max_len, file=sys.stderr)
    sys.exit(-1)

def check(condition: bool, message: str):
    if not condition:
        die(message)

CURRENT_COMMAND: None

def exec(command: str, machine='localhost', cwd=None, stdout=None, no_check=False) -> str:
    global CURRENT_COMMAND; CURRENT_COMMAND = command
    # Build command
    exec_prefix = ['bash', '-c'] if machine.lower() == 'localhost' else ['ssh', machine, '-t']
    if cwd is not None:
        command = f'cd {cwd} && {command}'
    cmd = [*exec_prefix, command]
    # Run
    stdout = (open(stdout, 'w') if stdout != PIPE else PIPE) if stdout is not None else None
    proc = subprocess.Popen(cmd, stdout=stdout)
    out, _ = proc.communicate()
    # Check success
    if not no_check and proc.returncode != 0: die(f'Command exit with code {proc.returncode}')
    # Return
    CURRENT_COMMAND = None
    return out.decode('utf-8') if stdout == PIPE else None



KW_ARGS = {}
REGISTERED_TASKS = {}
CURRENT_TASK = None

def register(func):
    # Check duplicate tasks
    if func.__name__ in REGISTERED_TASKS:
        (f, g) = (REGISTERED_TASKS[func.__name__].__code__, func.__code__)
        die(f'Duplicate task `{func.__name__}` at ./{f.co_filename}:{f.co_firstlineno} and ./{g.co_filename}:{g.co_firstlineno}')
    for n, p in signature(func).parameters.items():
        check(p.kind != Parameter.POSITIONAL_ONLY, f'Task `{func.__name__}` at ./{func.__code__.co_filename}:{func.__code__.co_firstlineno} should not have positional-only parameter `{n}`')
    REGISTERED_TASKS[func.__name__] = func
    return func

def run_task(t: str):
    global CURRENT_TASK
    parent_task = CURRENT_TASK
    CURRENT_TASK = REGISTERED_TASKS[t]
    # Check all positional arguments are specified
    kwargs = {}
    for n, p in signature(REGISTERED_TASKS[t]).parameters.items():
        if (p.kind == Parameter.POSITIONAL_OR_KEYWORD or p.kind == Parameter.KEYWORD_ONLY) and p.default == Parameter.empty:
            check(n in KW_ARGS, f'Flag `{n}` for task `{t} is missing`')
        if n in KW_ARGS:
            kwargs[n] = KW_ARGS[n]
    # Execute this task
    REGISTERED_TASKS[t](**kwargs)
    CURRENT_TASK = parent_task

def run():
    # Get all tasks
    tasks = [ arg for arg in sys.argv[1:] if not arg.startswith('--') ]
    for t in tasks:
        check(t in REGISTERED_TASKS, f'Unknown task `{t}`')
    # Build kwargs
    for arg in sys.argv[1:]:
        if arg.startswith('--'):
            op = arg[2:].split('=')
            KW_ARGS[op[0]] = op[1] if len(op) == 2 else True
    # Run tasks in order
    for t in tasks:
        run_task(t)
