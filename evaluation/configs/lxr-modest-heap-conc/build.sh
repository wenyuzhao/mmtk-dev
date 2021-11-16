#!/usr/bin/env bash
set -ex

source $(dirname $0)/../utils.sh

render_config

build_one jdk-b32k-$branch lxr,yield_and_roots_timer,satb_timer
build_one jdk-b64k-$branch lxr,yield_and_roots_timer,satb_timer,lxr_block_64k
build_one jdk-b129k-$branch lxr,yield_and_roots_timer,satb_timer,lxr_block_64k,mmtk/lxr_hole_counting