#!/usr/bin/env bash
set -ex

source $(dirname $0)/../utils.sh

render_config

# pushd ~/MMTk-Dev/mmtk-openjdk
# git checkout master
# popd
# build_one jdk-master

pushd ~/MMTk-Dev/mmtk-openjdk
git checkout fix-roots-leak
popd
build_one jdk-fixleak

# for i in $(seq 3 9); do
#     build_one jdk-lock-$i-$branch lxr_evac,mmtk/lxr_lock_$i
# done

# build_one jdk-block-64k-$branch lxr_evac,mmtk/lxr_block_64k
# build_one jdk-block-128k-$branch lxr_evac,mmtk/lxr_block_128k
# build_one jdk-block-256k-$branch lxr_evac,mmtk/lxr_block_256k
# build_one jdk-block-512k-$branch lxr_evac,mmtk/lxr_block_512k
# build_one jdk-block-1m-$branch lxr_evac,mmtk/lxr_block_1m