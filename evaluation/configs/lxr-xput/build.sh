#!/usr/bin/env bash
set -ex

source $(dirname $0)/../utils.sh

render_config


export PATH=$HOME/.cargo/bin:$PATH



pushd mmtk-core

# Shepherd version
# git checkout lxr-shepherd
# pushd ../mmtk-openjdk
# git checkout lxr-shepherd
# popd
# rake jdk:clean profile=release
# NURSERY_RATIO=1 build_one jdk-lxr-kc-$branch lxr
# pushd ../mmtk-openjdk
# git checkout lxr
# popd
# rake jdk:clean profile=release
# Shepherd version + bug fix
# git checkout lxr
# NURSERY_RATIO=1 build_one jdk-lxr-old-$branch lxr

# New GC trigger
# MAX_MATURE_DEFRAG_PERCENT=20 build_one jdk-lxr-new-trigger-2-$branch lxr,lxr_heap_health_guided_gc

# New Evacuation
# git checkout lxr-new-mature-evac
# build_one jdk-lxr-new-evac-$branch lxr,lxr_heap_health_guided_gc,mmtk/lxr_region_4m

popd

build_one jdk-lxr-$branch lxr,lxr_heap_health_guided_gc,mmtk/lxr_region_4m,mmtk/lxr_eager_defrag_selection
# build_one jdk-lxr-1m-$branch lxr,lxr_heap_health_guided_gc,mmtk/lxr_region_1m,mmtk/lxr_eager_defrag_selection

# build_one jdk-lxr-stw-submit-$branch lxr

# NURSERY_RATIO=1 build_one jdk-lxr-old-$branch lxr
# build_one jdk-lxr-$branch lxr,lxr_heap_health_guided_gc
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