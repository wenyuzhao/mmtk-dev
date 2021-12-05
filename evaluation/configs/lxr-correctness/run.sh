#!/usr/bin/env bash
set -x

hfac_args="8 4"

config=$(basename $(dirname $0))

pushd ~/MMTk-Dev

pkill -f java -u wenyuz -9

running runbms ./evaluation/results/log ~/MMTk-Dev/evaluation/configs/$config/config.yml $hfac_args &> ~/MMTk-Dev/lxr-correctness.log

popd