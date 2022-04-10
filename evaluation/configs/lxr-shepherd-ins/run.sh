#!/usr/bin/env bash
set -x

hfac_args="8 4"

config=$(basename $(dirname $0))

pushd ~/MMTk-Dev

running runbms ./evaluation/results/log ~/MMTk-Dev/evaluation/configs/$config/_config.yml 8 4 &> ~/_log

popd