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

z=""

# $latency_dump $branch large   1.5 2
# $latency_dump $branch huge    1.5 2

# $latency_dump $branch default 3    5    $z    "/usr/lib/jvm/temurin-17-amd64/bin/java"
# $latency_dump $branch large   3    2    $z    "/usr/lib/jvm/temurin-17-amd64/bin/java"
# $latency_dump $branch huge    3    2    $z    "/usr/lib/jvm/temurin-17-amd64/bin/java"

$latency_dump $branch default 3    5 $z "/home/wenyuz/MMTk-Dev/evaluation/configs/lxr-modest-heap-conc/jdk-ceece056/jdk/bin/java"
# $latency_dump $branch large   3    2
# $latency_dump $branch huge    3    2