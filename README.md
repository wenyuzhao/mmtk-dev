
# Getting Started

1. `git clone https://github.com/wenyuzhao/mmtk-dev.git`
2. Run `make init-jdk` once to initialize the repo and download dacapo benchmark suite.
   * For LXR developemnt, run `make init-jdk lxr=1`
   * Windiws or macOS users: Use docker by running `make init-jdk-docker` instead of `make init-jdk`.
     * Then just use the `./run-jdk` script as usual. It will build and run everything inside the docker container automatically.

## Further Instructions

* [OpenJDK Development](#openjdk-development)
* [JikesRVM Development](#jikesrvm-development)
* [V8 Development](#v8-development)
* [Benchmarking](#benchmarking)

# OpenJDK Development

```
./run-jdk --gc=SemiSpace --bench=lusearch --heap=500M --exploded --release -n 5 --build
```

Please run `./run-jdk --help` for all the available arguments

# JikesRVM Development

...WIP

# V8 Development

...WIP

# Benchmarking

1. Create the following config file as `./evaluation/configs/test.yml`. Please fix the commits and features fields in the file.
```yml
includes:
  - ./common/common.yml

overrides:
  heap_range: 3
  invocations: 40
  suites.dacapochopin-b00bfa9.minheap: g1

runtimes:
  jdk-mmtk-master:
    type: OpenJDK
    release: 11
    home: /$BUILDS/jdk-mmtk-master/jdk-11.0.19
    commits:
      mmtk-core: 1a9ba6090
      mmtk-openjdk: c681325
      openjdk: 91259ca9d60
  jdk-mmtk-dev:
    type: OpenJDK
    release: 11
    home: /$BUILDS/jdk-mmtk-dev/jdk-11.0.19
    commits:
      mmtk-core: 0febe9915
      mmtk-openjdk: c681325
      openjdk: 91259ca9d60
    features: mmtk/some_cargo_feature

configs:
  - jdk-mmtk-master|ss|common|tph
  - jdk-mmtk-dev|ss|common|tph
```
2. Commit the file
3. Run `./evaluation/manager.py build --config test` to build the openjdk builds
4. Run `./evaluation/manager.py rsync --remote boar.moma` to transfer the builds and configs to a experiment machine.
5. **On `boar.moma`**, run `./evaluation/manager.py run --config test --hfac 3x` to start benchmarking.
   * Please run `pip3 install -r requirements.txt --user` on the remote machine once to install necessary python packages
