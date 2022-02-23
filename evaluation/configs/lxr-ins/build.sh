#!/usr/bin/env bash
set -ex

source $(dirname $0)/../utils.sh

render_config

# build_one jdk-stw-$branch lxr_evac,instrumentation,no_fast_alloc
build_one jdk-$branch lxr,instrumentation