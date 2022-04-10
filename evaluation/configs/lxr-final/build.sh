#!/usr/bin/env bash
set -ex

source $(dirname $0)/../utils.sh

render_config

export PATH=$HOME/.cargo/bin:$PATH

# build_one jdk-lxr-$branch lxr,lxr_heap_health_guided_gc

# TRACE_THRESHOLD2=5 LOCK_FREE_BLOCKS=32 MAX_SURVIVAL_MB=128 SURVIVAL_PREDICTOR_WEIGHTED=1 build_one jdk-lxr-stw-$branch lxr_evac,lxr_heap_health_guided_gc

TRACE_THRESHOLD2=5 LOCK_FREE_BLOCKS=32 MAX_SURVIVAL_MB=128 SURVIVAL_PREDICTOR_WEIGHTED=1 build_one jdk-lxr-cm-$branch lxr_evac,lxr_cm,lxr_heap_health_guided_gc

TRACE_THRESHOLD2=5 LOCK_FREE_BLOCKS=32 MAX_SURVIVAL_MB=128 SURVIVAL_PREDICTOR_WEIGHTED=1 build_one jdk-lxr-lazy-$branch lxr_evac,lxr_lazy,lxr_heap_health_guided_gc

build_one jdk-ix-$branch
