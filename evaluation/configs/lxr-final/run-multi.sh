#!/usr/bin/env bash
set -x

config=$(basename $(dirname $0))

pkill -f java -u wenyuz -9

pushd ~/MMTk-Dev

running runbms ./evaluation/results/log ~/MMTk-Dev/evaluation/configs/$config/config.$1.yml 12 7 &> ~/_log
running runbms ./evaluation/results/log ~/MMTk-Dev/evaluation/configs/$config/config.$1-6.yml 12 12 &>> ~/_log

popd