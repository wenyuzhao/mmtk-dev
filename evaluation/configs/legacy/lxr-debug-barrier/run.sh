#!/usr/bin/env bash
set -x

hfac_args="12 12"

config=$(basename $(dirname $0))

pkill -f java -u wenyuz -9

pushd ~/MMTk-Dev

running runbms -p debug-barrier ./evaluation/results/log ~/MMTk-Dev/evaluation/configs/$config/config.yml 12 7 &> ~/_log

popd