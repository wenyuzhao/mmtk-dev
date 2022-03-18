#!/usr/bin/env bash
set -ex

source $(dirname $0)/../utils.sh

render_config

export PATH=$HOME/.cargo/bin:$PATH

# # Baseline LXR
# pushd mmtk-core
# git checkout lxr
# popd
# OPPORTUNISTIC_EVAC=1 OPPORTUNISTIC_EVAC_THRESHOLD=50 TRACE_THRESHOLD=30 MAX_MATURE_DEFRAG_PERCENT=15 INCS_LIMIT=10000 build_one jdk-lxr-stw lxr_evac,lxr_heap_health_guided_gc

# # # Baseline LXR with metadata
# pushd mmtk-core
# git checkout lxr-remset-invalidity-check
# popd
# OPPORTUNISTIC_EVAC=1 OPPORTUNISTIC_EVAC_THRESHOLD=50 TRACE_THRESHOLD=30 MAX_MATURE_DEFRAG_PERCENT=15 INCS_LIMIT=10000 build_one jdk-lxr-stw-meta lxr_evac,lxr_heap_health_guided_gc,mmtk/slow_edge_check

# # LXR with new validity checks
# OPPORTUNISTIC_EVAC=1 OPPORTUNISTIC_EVAC_THRESHOLD=50 TRACE_THRESHOLD=30 MAX_MATURE_DEFRAG_PERCENT=15 INCS_LIMIT=10000 build_one jdk-lxr-stw-check lxr_evac,lxr_heap_health_guided_gc







# Baseline LXR
pushd mmtk-core
git checkout lxr
popd
OPPORTUNISTIC_EVAC=1 OPPORTUNISTIC_EVAC_THRESHOLD=50 TRACE_THRESHOLD=30 MAX_MATURE_DEFRAG_PERCENT=15 INCS_LIMIT=10000 build_one jdk-lxr lxr,lxr_heap_health_guided_gc

# # Baseline LXR with metadata
pushd mmtk-core
git checkout lxr-remset-invalidity-check
popd
OPPORTUNISTIC_EVAC=1 OPPORTUNISTIC_EVAC_THRESHOLD=50 TRACE_THRESHOLD=30 MAX_MATURE_DEFRAG_PERCENT=15 INCS_LIMIT=10000 build_one jdk-lxr-meta lxr,lxr_heap_health_guided_gc,mmtk/slow_edge_check

# LXR with new validity checks
OPPORTUNISTIC_EVAC=1 OPPORTUNISTIC_EVAC_THRESHOLD=50 TRACE_THRESHOLD=30 MAX_MATURE_DEFRAG_PERCENT=15 INCS_LIMIT=10000 build_one jdk-lxr-check lxr,lxr_heap_health_guided_gc
