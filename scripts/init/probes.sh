#!/usr/bin/env bash

set -e

declare -r script_dir=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )

if [ -d "$script_dir/../../evaluation/probes" ]; then
    echo "probes already exists."
    exit 0
fi

mkdir -p $script_dir/../../evaluation/probes

pushd $script_dir/../../evaluation/probes
    wget https://github.com/anupli/probes/releases/download/20230127-snapshot/librust_mmtk_probe.so
    wget https://github.com/anupli/probes/releases/download/20230127-snapshot/librust_mmtk_probe_32.so
    wget https://github.com/anupli/probes/releases/download/20230127-snapshot/probes-java6.jar
    wget https://github.com/anupli/probes/releases/download/20230127-snapshot/probes.jar
popd
