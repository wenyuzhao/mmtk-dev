#!/usr/bin/env bash
set -x

hfac_args="12 0"

config=$(basename $(dirname $0))

pushd ~/MMTk-Dev

running runbms ./evaluation/results/log ~/MMTk-Dev/evaluation/configs/$config/config.g1.yml 12 12 &> ~/_log

popd