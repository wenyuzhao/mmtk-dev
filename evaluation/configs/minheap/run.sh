#!/usr/bin/env bash
set -x

config=$(basename $(dirname $0))

pushd ~/MMTk-Dev

pkill -f java -u wenyuz -9

running minheap ~/MMTk-Dev/evaluation/configs/$config/_config.yml ~/MMTk-Dev/minheap.10.log &> ~/_log

popd