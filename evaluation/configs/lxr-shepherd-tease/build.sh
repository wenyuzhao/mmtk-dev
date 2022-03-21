#!/usr/bin/env bash
set -ex

source $(dirname $0)/../utils.sh

render_config


export PATH=$HOME/.cargo/bin:$PATH

NURSERY_RATIO=1 build_one jdk-lxr-stw-$branch lxr_evac
NURSERY_RATIO=1 build_one jdk-lxr-lazy-$branch lxr_evac,lxr_lazy
NURSERY_RATIO=1 build_one jdk-lxr-cm-$branch lxr_evac,lxr_cm
NURSERY_RATIO=1 build_one jdk-lxr-$branch lxr
