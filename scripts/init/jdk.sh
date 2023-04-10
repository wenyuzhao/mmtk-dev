#!/usr/bin/env bash

set -e

declare lxr=0

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

if [ ! -f "mmtk-openjdk/README.md" ]; then
    git submodule update --init --remote mmtk-openjdk
    pushd  mmtk-openjdk
        git checkout master
    popd
fi

if [ ! -f "openjdk/LICENSE" ]; then
    git submodule update --init --remote openjdk
    pushd openjdk
        git checkout jdk-11.0.19+1-mmtk
    popd
fi

if ((lxr)); then
    if [ ! -f "mmtk-openjdk/README.md" ]; then
        echo "mmtk-openjdk does not exist."
        exit -1
    fi
    if [ ! -f "openjdk/LICENSE" ]; then
        echo "openjdk does not exist."
        exit -1
    fi

    pushd mmtk-openjdk
        git remote add wenyu https://github.com/wenyuzhao/mmtk-openjdk.git
        git fetch wenyu
        git checkout -b lxr wenyu/lxr
    popd

    pushd openjdk
        git checkout jdk-11.0.19+1-mmtk-lxr
    popd
fi
