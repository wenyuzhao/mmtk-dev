#!/usr/bin/env bash
set -x

config=$(basename $(dirname $0))

pkill -f java -u wenyuz -9

pushd ~/MMTk-Dev

running runbms -p colored-ptr ./evaluation/results/log ~/MMTk-Dev/evaluation/configs/$config/config.yml 12 6 &> ~/_log

popd