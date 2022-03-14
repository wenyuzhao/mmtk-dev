#!/usr/bin/env bash
set -x

hfac_args="8 4"

config=$(basename $(dirname $0))

pkill -f java -u wenyuz -9

pushd ~/MMTk-Dev

running runbms ./evaluation/results/log ~/MMTk-Dev/evaluation/configs/$config/_config.yml $hfac_args &> ~/_log

popd