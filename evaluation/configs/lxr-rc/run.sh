#!/usr/bin/env bash
set -x

hfac_args="12 0"

config=$(basename $(dirname $0))

pushd ~/MMTk-Dev

running runbms ./evaluation/results/log ~/MMTk-Dev/evaluation/configs/$config/_config.yml 12 0 &> ~/_log

popd