#!/usr/bin/env bash
set -ex

source $(dirname $0)/../utils.sh

render_config


export PATH=$HOME/.cargo/bin:$PATH



rake jdk:test gc=Immix heap=3287M noc1=1 bench=lusearch profile=release n=5 features=lxr_heap_health_guided_gc,lxr_rc_only
rake bench:cp name=$config/jdk-lxr-rc-$branch

# rake jdk:test gc=Immix heap=2287M noc1=1 bench=lusearch profile=release n=5 features=lxr,lxr_heap_health_guided_gc,mmtk/lxr_incremental_defrag SIMPLE_INCREMENTAL_DEFRAG=8
# rake bench:cp name=$config/jdk-lxr-rc-evac-$branch

rake jdk:test gc=Immix heap=20G noc1=1 bench=lusearch n=5 profile=release features=lxr,lxr_heap_health_guided_gc,mmtk/lxr_region_4m SIMPLE_INCREMENTAL_DEFRAG=8 SIMPLE_INCREMENTAL_DEFRAG_MULTIPLIER=8 NURSERY_BLOCKS=8192
rake bench:cp name=$config/jdk-lxr-rc-evac-4m-$branch


# rake jdk:test gc=Immix heap=2287M noc1=1 bench=lusearch profile=release n=5 features=lxr_heap_health_guided_gc,lxr_rc_only,mmtk/lxr_enable_initial_alloc_limit
# rake bench:cp name=$config/jdk-lxr-rc-initalloc-$branch

# build_one jdk-lxr-stw-submit-$branch lxr

# NURSERY_RATIO=1 build_one jdk-lxr-old-$branch lxr
# OPPORTUNISTIC_EVAC=1 OPPORTUNISTIC_EVAC_THRESHOLD=50 TRACE_THRESHOLD=30 MAX_MATURE_DEFRAG_PERCENT=15 INCS_LIMIT=10000 build_one jdk-lxr-$branch lxr,lxr_heap_health_guided_gc
# MAX_MATURE_DEFRAG_PERCENT=20 OPPORTUNISTIC_EVAC=1 OPPORTUNISTIC_EVAC_THRESHOLD=50 build_one jdk-lxr-$branch lxr,lxr_heap_health_guided_gc
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