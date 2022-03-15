#!/usr/bin/env bash
set -ex

source $(dirname $0)/../utils.sh

render_config

export PATH=$HOME/.cargo/bin:$PATH

NURSERY_RATIO=1 build_one jdk-lxr-$branch lxr,log_pause_time
