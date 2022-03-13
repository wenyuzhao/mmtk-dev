#!/usr/bin/env bash
set -ex

source $(dirname $0)/../utils.sh

render_config

# build_one jdk-$branch

NURSERY_RATIO=1 build_one jdk-lxr-old-fixleak-$branch lxr
# OPPORTUNISTIC_EVAC=1 OPPORTUNISTIC_EVAC_THRESHOLD=50 MAX_MATURE_DEFRAG_PERCENT=10 build_one jdk-lxr-fixleak-$branch lxr,lxr_heap_health_guided_gc