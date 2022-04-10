#!/usr/bin/env bash
set -ex

source $(dirname $0)/../utils.sh

render_config


export PATH=$HOME/.cargo/bin:$PATH

build_one jdk-lxr-$branch lxr,lxr_heap_health_guided_gc
build_one jdk-lxr-rc4-$branch lxr,lxr_heap_health_guided_gc,mmtk/lxr_rc_bits_4
build_one jdk-lxr-rc8-$branch lxr,lxr_heap_health_guided_gc,mmtk/lxr_rc_bits_8
build_one jdk-lxr-block16-$branch lxr,lxr_heap_health_guided_gc,mmtk/lxr_block_16k
build_one jdk-lxr-block64-$branch lxr,lxr_heap_health_guided_gc,mmtk/lxr_block_64k