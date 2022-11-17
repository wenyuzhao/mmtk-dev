#!/usr/bin/env bash
set -x

hfac_args="12 12"

config=$(basename $(dirname $0))

pkill -f java -u wenyuz -9

pushd ~/MMTk-Dev

./run-jdk.py --gc=LXR --bench=lusearch --heap=105M -n 5 --no-c1 --build --release --cp-bench=lxr
./run-jdk.py --gc=LXR --bench=lusearch --heap=105M -n 5 --no-c1 --build --release --features mmtk/force_zeroing --cp-bench=lxr-zero
./run-jdk.py --gc=LXR --bench=lusearch --heap=105M -n 5 --no-c1 --build --release --features mmtk/large_tlab --cp-bench=lxr-alloc-fix

popd