#!/usr/bin/env bash
set -x

hfac_args="8 4 8"

config=$(basename $(dirname $0))

pushd ~/MMTk-Dev

running runbms ./evaluation/results/log ~/MMTk-Dev/evaluation/configs/$config/_config.yml $hfac_args --skip-oom 1 --skip-timeout 1 &> ~/_log

popd