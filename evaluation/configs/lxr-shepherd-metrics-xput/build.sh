#!/usr/bin/env bash
set -ex

source $(dirname $0)/../utils.sh

render_config


export PATH=$HOME/.cargo/bin:$PATH

# NURSERY_RATIO=1 build_one jdk-lxr-$branch lxr
# NURSERY_RATIO=1 build_one jdk-lxr-rc4-$branch lxr,mmtk/lxr_rc_bits_4
NURSERY_RATIO=1 build_one jdk-lxr-rc8-$branch lxr,mmtk/lxr_rc_bits_8
NURSERY_RATIO=1 build_one jdk-lxr-block16-$branch lxr,mmtk/lxr_block_16k
NURSERY_RATIO=1 build_one jdk-lxr-block64-$branch lxr,mmtk/lxr_block_64k