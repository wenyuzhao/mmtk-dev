
# Getting Started

1. `git clone https://github.com/wenyuzhao/MMTk-Dev.git --recursive`
2. Run `rake init` once to initialize the repo.

## Instructions

* [OpenJDK](#openjdk)
* [JikesRVM](#jikesrvm)
* [V8](#v8)

# OpenJDK

```
usage: run-jdk.py --gc GC --bench BENCH --heap HEAP [--profile PROFILE]
                  [--release] [--build] [--config] [-n ITER] [--no-c1]
                  [--no-c2] [--mu [MU]] [--threads [THREADS]] [--gdb] [-h]

MMTk-OpenJDK Runner.

Example: ./run-jdk.py --gc=SemiSpace --bench=xalan --heap=100M --build

required arguments:
  --gc GC               GC plan. e.g. SemiSpace
  --bench BENCH         DaCapo benchmark name
  --heap HEAP           Heap size

optional arguments:
  --profile PROFILE     Specify build profile. Default to fastdebug
  --release             Use release profile. This overrides --profile.
  --build               Build OpenJDK
  --config              Config OpenJDK
  -n ITER, --iter ITER  Number of iterations
  --no-c1               Disable C1 compiler
  --no-c2               Disable C2 compiler
  --mu [MU]             Fix mutators
  --threads [THREADS]   Fix GC workers
  --gdb                 Launch GDB
  -h, --help            Show this help message and exit
```

# Benchmarking

WIP

# JikesRVM

1. `rake jks:build profile=RBaseBaseSemiSpace`
2. `rake jks:test profile=RBaseBaseSemiSpace heap=100M bench=xalan`
    * Run with multiple iterations: `rake jks:test profile=RBaseBaseSemiSpace heap=100M bench=xalan n=5`

# V8

...WIP
