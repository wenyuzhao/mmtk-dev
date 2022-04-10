#!/usr/bin/env bash
set -ex

source $(dirname $0)/../utils.sh

render_config

export PATH=$HOME/.cargo/bin:$PATH

build_one jdk-lxr-$branch lxr,lxr_heap_health_guided_gc,mmtk/pause_time
