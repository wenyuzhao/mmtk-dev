
# Getting Started

1. `git clone https://github.com/wenyuzhao/MMTk-Dev.git`
2. Run `./scripts/init-mmtk-jdk.sh` once to initialize the repo.

## Instructions

* [OpenJDK](#openjdk)
* [JikesRVM](#jikesrvm)
* [V8](#v8)

# OpenJDK

```
./run-jdk --gc=SemiSpace --bench=lusearch --heap=500M --exploded --release -n 5 --build 
```

Please run `./run-jdk --help` for all the available arguments

# Benchmarking

1. Produce two different builds:
  1. `./run-jdk --gc=Immix --bench=xalan --heap=100M --build --release --cp-bench master`
  2. `./run-jdk --gc=Immix --bench=xalan --heap=100M --build --release --features dev --cp-bench dev`
  3. You will get two builds under _evaluation/builds_: _jdk-mmtk-<commit>-master_ and _jdk-mmtk-<commit>-dev_
2. Add a config file to _evaluation/configs/<config>/config.yml_
3. Rsync files to a remote machine: `./scripts/bench-rsync.py --machine deer.moma`
4. Run benchmarks

# JikesRVM

...WIP

# V8

...WIP
