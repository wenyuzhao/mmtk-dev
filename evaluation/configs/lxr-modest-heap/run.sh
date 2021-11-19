#!/usr/bin/env bash
set -x

hfac_args="8 4"

config=$(basename $(dirname $0))

pushd ~/MMTk-Dev

pkill -f java -u wenyuz -9

running runbms ./evaluation/results/log ~/MMTk-Dev/evaluation/configs/$config/_config.yml $hfac_args --skip-oom 1 --skip-timeout 1 &> ~/_log

popd