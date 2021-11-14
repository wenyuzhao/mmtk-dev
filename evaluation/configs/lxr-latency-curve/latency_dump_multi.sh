#!/usr/bin/env bash
set -e

if [ $# -lt 1 ]; then
    echo "Usage: $0 [git-hash]"
    echo ""
    echo "e.g. ./lagency_dump_multi.sh a9feb14"
    exit
fi

branch=$1

latency_dump=~/MMTk-Dev/evaluation/configs/lxr-latency-curve/latency_dump.sh

$latency_dump $branch default 3
$latency_dump $branch large   3
$latency_dump $branch huge    3
$latency_dump $branch large   1.5
$latency_dump $branch huge    1.5