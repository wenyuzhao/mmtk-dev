#!/usr/bin/env bash
set -ex

source $(dirname $0)/../utils.sh

render_config

NURSERY_RATIO=1 build_one jdk-lxr-old-$branch lxr,instrumentation
# OPPORTUNISTIC_EVAC=1 OPPORTUNISTIC_EVAC_THRESHOLD=50 build_one jdk-lxr-stw-$branch lxr_evac,lxr_heap_health_guided_gc
# MAX_MATURE_DEFRAG_PERCENT=20 OPPORTUNISTIC_EVAC=1 OPPORTUNISTIC_EVAC_THRESHOLD=50 build_one jdk-lxr-$branch lxr_evac,instrumentation,lxr_heap_health_guided_gc
# MAX_MATURE_DEFRAG_PERCENT=20 OPPORTUNISTIC_EVAC=1 OPPORTUNISTIC_EVAC_THRESHOLD=50 build_one jdk-lxr-stw-$branch lxr_evac,lxr_heap_health_guided_gc

# NURSERY_RATIO=1 build_one jdk-lxr-stw-old-$branch lxr_evac

# for i in $(seq 3 9); do
#     build_one jdk-lock-$i-$branch lxr_evac,mmtk/lxr_lock_$i
# done

# build_one jdk-block-64k-$branch lxr_evac,mmtk/lxr_block_64k
# build_one jdk-block-128k-$branch lxr_evac,mmtk/lxr_block_128k
# build_one jdk-block-256k-$branch lxr_evac,mmtk/lxr_block_256k
# build_one jdk-block-512k-$branch lxr_evac,mmtk/lxr_block_512k
# build_one jdk-block-1m-$branch lxr_evac,mmtk/lxr_block_1m