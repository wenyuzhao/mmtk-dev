#!/usr/bin/env bash
set -ex

source $(dirname $0)/../utils.sh

render_config

# build_one jdk-$branch

# NURSERY_RATIO=1 build_one jdk-lxr-old-fixleak-$branch lxr

# TRACE_THRESHOLD=30 INCS_LIMIT=20000 build_one jdk-lxr-rc-$branch lxr_rc_only

build_one jdk-lxr-$branch lxr,lxr_heap_health_guided_gc

# pushd ~/MMTk-Dev/mmtk-core
# git checkout lxr
# popd

# OPPORTUNISTIC_EVAC=1 OPPORTUNISTIC_EVAC_THRESHOLD=50 TRACE_THRESHOLD=30 INCS_LIMIT=20000 build_one jdk-lxr-$branch lxr,lxr_heap_health_guided_gc