#!/usr/bin/env bash
set -ex

source $(dirname $0)/../utils.sh

render_config

export PATH=$HOME/.cargo/bin:$PATH

rake jdk:test gc=GenCopy heap=400M noc1=1 bench=lusearch profile=release n=5
rake bench:cp name=$config/jdk-gencopy-$branch
