#!/usr/bin/env bash

set -ex

if [ -d "evaluation/probes" ]; then
    echo "probes already exists."
    exit -1
fi

mkdir -p evaluation/probes

pushd evaluation/probes
    wget https://github.com/anupli/probes/releases/download/20230127-snapshot/librust_mmtk_probe.so
    wget https://github.com/anupli/probes/releases/download/20230127-snapshot/librust_mmtk_probe_32.so
    wget https://github.com/anupli/probes/releases/download/20230127-snapshot/probes-java6.jar
    wget https://github.com/anupli/probes/releases/download/20230127-snapshot/probes.jar
popd
