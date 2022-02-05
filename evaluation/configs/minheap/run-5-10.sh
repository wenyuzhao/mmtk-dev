#!/usr/bin/env bash
set -x

config=$(basename $(dirname $0))

pushd ~/MMTk-Dev

pkill -f java -u wenyuz -9

running minheap ~/MMTk-Dev/evaluation/configs/$config/config.5.yml ~/MMTk-Dev/minheap.5.noweak.log &> ~/_log

echo '' >> ~/_log
echo '' >> ~/_log
echo '' >> ~/_log
echo '---' >> ~/_log
echo '' >> ~/_log
echo '' >> ~/_log
echo '' >> ~/_log

running minheap ~/MMTk-Dev/evaluation/configs/$config/config.10.yml ~/MMTk-Dev/minheap.10.noweak.log &>> ~/_log

popd