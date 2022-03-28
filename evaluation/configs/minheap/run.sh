#!/usr/bin/env bash
set -x

config=$(basename $(dirname $0))

pushd ~/MMTk-Dev

pkill -f java -u wenyuz -9

running minheap -a 5 ~/MMTk-Dev/evaluation/configs/$config/_config.yml ~/MMTk-Dev/_minheap.y.yml &> ~/_log

popd