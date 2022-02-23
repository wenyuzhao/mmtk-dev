#!/usr/bin/env bash
set -x

config=$(basename $(dirname $0))

pushd ~/MMTk-Dev

pkill -f java -u wenyuz -9

running minheap -a 5 ~/MMTk-Dev/evaluation/configs/$config/config.$1.yml ~/MMTk-Dev/minheap.$1.yml &> ~/MMTk-Dev/minheap.$1.log

popd