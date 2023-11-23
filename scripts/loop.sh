#!/usr/bin/env bash

set -ex

echo "" > x.log

for i in {0..10}; do
echo $i
    ./run-jdk --gc=LXR --bench=xalan --heap=34M -n 5 -xbr &> x.log
done

# cat x.log | grep "GC\|panic\|ERROR\|ERR\|object"