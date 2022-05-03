#!/usr/bin/env bash
set -x

hfac_args="12 12"

config=$(basename $(dirname $0))

pkill -f java -u wenyuz -9

pushd ~/MMTk-Dev

# 1.3x lusearch, G1/LXR/Shen./Shen78
running runbms -i 15 ./evaluation/results/log ~/MMTk-Dev/evaluation/configs/$config/config.punch.yml 32 7 &> ~/_log
# 1.3x luseach, Shen10x
# running runbms -i 15 ./evaluation/results/log ~/MMTk-Dev/evaluation/configs/$config/config.shen10x.yml 12 12 &>> ~/_log
# 2x LXR
# running runbms -i 15  ./evaluation/results/log ~/MMTk-Dev/evaluation/configs/$config/_config.yml 12 7 &>> ~/_log

popd