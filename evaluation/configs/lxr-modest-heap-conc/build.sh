#!/usr/bin/env bash
set -ex

source $(dirname $0)/../utils.sh

render_config

build_one jdk-$branch lxr,yield_and_roots_timer,work_packet_timer,satb_timer