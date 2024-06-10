# `running-ng` configs

This directory contains all the running ng configs.

Note that the config files cannot be directly executed by `running-ng`. The ` mmtk-jdk bench` wrapper script is required to pre-process the config files.

## Example Usage: Reproduce the results in LXR PLDI paper

1. Install the wrapper script: `poetry install`
2. Launch poetry shell: `poetry shell`
3. Produce JDK builds: `mmtk-jdk bench build --config lxr-pldi/xput`
4. Rsync all the necessary files to a evaluation machine: `mmtk-jdk bench rsync --remote bear.moma`
5. **On `bear.moma`:** Start evaluation: `mmtk-jdk bench run --config lxr-pldi/xput`

## Extensions to the `running-ng` config-file format

### 1. Pre-defined environment variables

* **`BUILDS`**: Absolute path pointing to _$MMTK_DEV/evaluation/builds_, containing all the automatically produced jdk builds.
* **`CONFIGS`**: Absolute path pointing to _$MMTK_DEV/evaluation/configs_.
* **`CONFIG`**: Absolute path pointing to the current config file.
* **`ID_PREFIX`**: The string being prepended to the runid. This will also be passed as the running `-p` cli parameter.

```yml
runtimes:
  jdk-mmtk:
    type: OpenJDK
    release: 11
    home: $BUILDS/jdk-mmtk/jdk-11.0.19
```

### 2. `runtimes`: Emeded commits and rust-features

`mmtk-jdk bench build` will automatically parse these fields, checkout the commits, enable the corresponding rust flags, and produce the JDK build.

```yml
runtimes:
  jdk-mmtk-defeatured:
    type: OpenJDK
    release: 11
    home: $BUILDS/jdk-mmtk-defeatured/jdk-11.0.19
    commits:
      mmtk-core: 8f76a35015
      mmtk-openjdk: 83f2d3aa56b
      openjdk: bc9669aaed
    features: no_weak_refs
```

### 3. `runtimes`: Test commands

By default, `mmtk-jdk bench build` runs _DaCapo-fop_ using the produced JDK build with with _Immix GC_, to check the build is functional.

**To run with a different gc:** `mmtk-jdk bench build --config <config-name> --gc LXR`

**To run with custom test command:**

```yml
runtimes:
  jdk-mmtk:
    type: OpenJDK
    release: 11
    home: $BUILDS/jdk-mmtk/jdk-11.0.19
    commits:
      mmtk-core: 8f76a35015
      mmtk-openjdk: 83f2d3aa56b
      openjdk: bc9669aaed
    test-command: ./openjdk/build/linux-x86_64-normal-server-release/jdk/bin/java -version
```

### 4. `runtimes`: Exploded build

To produce exploded jdk, you must specify the custom `test-command` and update `home` correctly.

```yml
runtimes:
  jdk-mmtk-x:
    type: OpenJDK
    release: 11
    home: $BUILDS/jdk-mmtk-x/jdk
    commits:
      mmtk-core: 8f76a35015
      mmtk-openjdk: 83f2d3aa56b
      openjdk: bc9669aaed
    exploded: true
    test-command: ./openjdk/build/linux-x86_64-normal-server-release/jdk/bin/java -version
```

### 5. Embeded run args

Putting `hfac: 2x` at the root of the config file will make `mmtk-jdk bench run` to use 2x heap factor.

Available hfac values: `1x`, `1.3x`, `2x`, `3x`, or dash separated raw numbers like `12-2-3-5`.

Alternatively, run `mmtk-jdk bench run --config <config-name> --hfac 2x` to override the embeded value in the file.

To use a totally different run command, put `command: ...` at the root of the config file:

```yml
command: running minheap --attempts 5 $CONFIG ./minheap.yml
```

