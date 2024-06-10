#!/usr/bin/env bash
set -x

hfac_args="12 12"

config=$(basename $(dirname $0))

pkill -f java -u wenyuz -9

pushd ~/MMTk-Dev

./run-jdk.py --gc=LXR --bench=lusearch --heap=500M -n 5 --no-c1 --build --release --cp-bench=lxr

./run-jdk.py --gc=LXR --bench=lusearch --heap=500M -n 5 --no-c1 --build --release --features mmtk/lxr_block_128k --cp-bench=lxr-block128k
./run-jdk.py --gc=LXR --bench=lusearch --heap=500M -n 5 --no-c1 --build --release --features mmtk/lxr_block_512k --cp-bench=lxr-block512k

./run-jdk.py --gc=LXR --bench=lusearch --heap=500M -n 5 --no-c1 --build --release --features mmtk/lxr_line_512b --cp-bench=lxr-line512b
./run-jdk.py --gc=LXR --bench=lusearch --heap=500M -n 5 --no-c1 --build --release --features mmtk/lxr_line_1k --cp-bench=lxr-line1k

popd