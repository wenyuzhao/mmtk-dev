# running-ng configs

This directory contains all the running ng configs.

Note that the config files cannot be directly executed by `running-ng`. The ` mmtk-jdk bench` wrapper script is required to pre-process the config files.

# Example Usage: Reproduce the throughput results in LXR PLDI paper:

1. Install the wrapper script: `poetry install`
2. Launch poetry shell: `poetry shell`
3. Produce JDK builds: `mmtk-jdk bench build --config lxr-pldi/xput`
4. Rsync all the necessary files to a evaluation machine: `mmtk-jdk bench rsync --remote bear.moma`
5. **On `bear.moma`:** Start evaluation: `mmtk-jdk bench run --config lxr-pldi/xput`

