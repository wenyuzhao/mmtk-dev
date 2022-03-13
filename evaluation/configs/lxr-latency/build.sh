#!/usr/bin/env bash
set -ex

source $(dirname $0)/../utils.sh

render_config

# build_one jdk-b32k-mixcmrc-$branch lxr,yield_and_roots_timer,satb_timer
# build_one jdk-b32k-old-$branch lxr,yield_and_roots_timer,satb_timer
# build_one jdk-$branch lxr,yield_and_roots_timer,satb_timer
# build_one jdk-b32k-stw-$branch lxr_evac,yield_and_roots_timer,satb_timer


# NURSERY_RATIO=1 build_one jdk-lxr-old-$branch lxr
OPPORTUNISTIC_EVAC=1 OPPORTUNISTIC_EVAC_THRESHOLD=50 MAX_MATURE_DEFRAG_PERCENT=10 build_one jdk-lxr-$branch lxr,lxr_heap_health_guided_gc