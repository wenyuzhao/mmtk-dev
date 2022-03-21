#!/usr/bin/env bash
set -x

hfac_args="12 12"

config=$(basename $(dirname $0))

pushd ~/MMTk-Dev

pkill -f java -u wenyuz -9

# Pause 3X elk-2022-03-20-Sun-233255
running runbms ./evaluation/results/log ~/MMTk-Dev/evaluation/configs/lxr-shepherd-pauses/_config.yml 12 12 &> ~/_log

# Pause Shen 10X elk-2022-03-21-Mon-042713
running runbms ./evaluation/results/log ~/MMTk-Dev/evaluation/configs/lxr-shepherd-pauses/config.shen10x.yml 12 12 &> ~/_log2

# Pause 2X elk-2022-03-21-Mon-062551
running runbms ./evaluation/results/log ~/MMTk-Dev/evaluation/configs/lxr-shepherd-pauses/config.2x.yml 12 12 &> ~/_log3

# Latency 3X Shen 7/8
running runbms ./evaluation/results/log ~/MMTk-Dev/evaluation/configs/lxr-shepherd-latency/config.shen78.lu.yml 12 12 &> ~/_log4

# Latency 2X
running runbms ./evaluation/results/log ~/MMTk-Dev/evaluation/configs/lxr-shepherd-latency/config.2x.yml 12 12 &> ~/_log5

# latency 2x lusearch deer-2022-03-21-Mon-100248


popd