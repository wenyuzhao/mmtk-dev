#!/usr/bin/env bash
set -ex

source $(dirname $0)/../utils.sh

render_config

build_one jdk-b32k-$branch lxr,yield_and_roots_timer,satb_timer
build_one jdk-b64k-$branch lxr,yield_and_roots_timer,satb_timer,mmtk/lxr_block_64k
build_one jdk-b64k-hole-$branch lxr,yield_and_roots_timer,satb_timer,mmtk/lxr_block_64k,mmtk/lxr_hole_counting
build_one jdk-b64k-stw-$branch lxr_evac,yield_and_roots_timer,satb_timer,mmtk/lxr_block_64k