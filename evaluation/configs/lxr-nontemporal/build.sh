#!/usr/bin/env bash
set -ex

source $(dirname $0)/../utils.sh

render_config


export PATH=$HOME/.cargo/bin:$PATH

# OPPORTUNISTIC_EVAC=1 OPPORTUNISTIC_EVAC_THRESHOLD=50 TRACE_THRESHOLD=30 MAX_MATURE_DEFRAG_PERCENT=15 INCS_LIMIT=10000 build_one jdk-lxr-nt-$branch lxr,lxr_heap_health_guided_gc

OPPORTUNISTIC_EVAC=1 OPPORTUNISTIC_EVAC_THRESHOLD=50 TRACE_THRESHOLD=30 MAX_MATURE_DEFRAG_PERCENT=15 INCS_LIMIT=10000 build_one jdk-lxr-$branch lxr,lxr_heap_health_guided_gc