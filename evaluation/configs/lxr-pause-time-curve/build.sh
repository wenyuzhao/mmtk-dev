#!/usr/bin/env bash
set -ex

source $(dirname $0)/../utils.sh

render_config

# build_one jdk-b32k-mixcmrc-$branch lxr,yield_and_roots_timer,satb_timer
# build_one jdk-b32k-old-$branch lxr,yield_and_roots_timer,satb_timer
build_one jdk-$branch lxr,yield_and_roots_timer,satb_timer,mmtk/pause_time
# build_one jdk-b32k-stw-$branch lxr_evac,yield_and_roots_timer,satb_timer