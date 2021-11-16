#!/usr/bin/env bash
set -ex

source $(dirname $0)/../utils.sh

render_config

build_one jdk-$branch lxr,instrumentation