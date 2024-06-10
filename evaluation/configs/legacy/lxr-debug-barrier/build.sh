#!/usr/bin/env bash
set -x

hfac_args="12 12"

config=$(basename $(dirname $0))

pkill -f java -u wenyuz -9

pushd ~/MMTk-Dev

# ./run-jdk.py --gc=LXR --bench=lusearch --heap=105M -n 5 --no-c1 --build --release --cp-bench=lxr
# ./run-jdk.py --gc=LXR --bench=lusearch --heap=105M -n 5 --no-c1 --build --release --features mmtk/force_zeroing --cp-bench=lxr-zero
# ./run-jdk.py --gc=LXR --bench=lusearch --heap=105M -n 5 --no-c1 --build --release --features mmtk/large_tlab --cp-bench=lxr-alloc-fix

./run-jdk.py --gc=Immix --bench=h2 --heap=2370M -n 5 --no-c1 --build  --release --features barrier_measurement,mmtk/large_tlab,mmtk/lxr_lock_8 --cp-bench=ix-largetlab-fieldbarrier-lock8
./run-jdk.py --gc=Immix --bench=h2 --heap=2370M -n 5 --no-c1 --build  --release --features barrier_measurement,mmtk/large_tlab,mmtk/lxr_lock_7 --cp-bench=ix-largetlab-fieldbarrier-lock7
./run-jdk.py --gc=Immix --bench=h2 --heap=2370M -n 5 --no-c1 --build  --release --features barrier_measurement,mmtk/large_tlab,mmtk/lxr_lock_6 --cp-bench=ix-largetlab-fieldbarrier-lock6
./run-jdk.py --gc=Immix --bench=h2 --heap=2370M -n 5 --no-c1 --build  --release --features barrier_measurement,mmtk/large_tlab,mmtk/lxr_lock_5 --cp-bench=ix-largetlab-fieldbarrier-lock5
./run-jdk.py --gc=Immix --bench=h2 --heap=2370M -n 5 --no-c1 --build  --release --features barrier_measurement,mmtk/large_tlab,mmtk/lxr_lock_4 --cp-bench=ix-largetlab-fieldbarrier-lock4
./run-jdk.py --gc=Immix --bench=h2 --heap=2370M -n 5 --no-c1 --build  --release --features barrier_measurement,mmtk/large_tlab,mmtk/lxr_lock_3 --cp-bench=ix-largetlab-fieldbarrier-lock3

popd