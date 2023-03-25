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


if [ ! -f "mmtk-core/Cargo.toml" ]; then
    git submodule update --init --remote mmtk-core
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

declare -r script_dir=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )
pushd $script_dir/../..
  pip3 install -r requirements.txt --user
popd