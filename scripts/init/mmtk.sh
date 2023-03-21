#!/usr/bin/env bash

set -ex

lxr=0
probes=0

while [[ $# -gt 0 ]]; do
  case $1 in
    --lxr)
      lxr=1
      shift
      ;;
    *)
      shift
      ;;
  esac
done


if [ ! -f "mmtk-core/Cargo.toml" ]; then
    git submodule update --init mmtk-core
    pushd mmtk-core
        git checkout master
    popd
fi

if ((lxr)); then
    if [ ! -f "mmtk-core/Cargo.toml" ]; then
        echo "mmtk-core does not exist."
        exit -1
    fi
    pushd mmtk-core
        git remote add wenyu git@github.com:wenyuzhao/mmtk-core.git
        git fetch wenyu
        git checkout -b lxr wenyu/lxr
    popd
fi
