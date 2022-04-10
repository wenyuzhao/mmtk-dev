#!/usr/bin/env bash
set -x

hfac_args="12 12"

config=$(basename $(dirname $0))

pushd ~/MMTk-Dev

pkill -f java -u wenyuz -9

running runbms ./evaluation/results/log ~/MMTk-Dev/evaluation/configs/$config/config.2x.lu.yml 12 7 &> ~/_log
running runbms ./evaluation/results/log ~/MMTk-Dev/evaluation/configs/$config/config.2x.other.yml 12 7 &>> ~/_log
# running runbms ./evaluation/results/log ~/MMTk-Dev/evaluation/configs/$config/_config.2.yml 10 9 16 --skip-oom 1 --skip-timeout 1 &> ~/_log

popd