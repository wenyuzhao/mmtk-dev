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

# git submodule update --init mmtk-core mmtk-openjdk openjdk # evaluation/probes

if ((lxr)); then
    if [ ! -d "mmtk-core" ]; then
        echo "mmtk-core does exist."
        exit -1
    fi
    pushd mmtk-core
    git remote add wenyu https://github.com/wenyuzhao/mmtk-core
    git fetch wenyu
    git checkout -b lxr wenyu/lxr
    popd

    if [ ! -d "mmtk-openjdk" ]; then
        echo "mmtk-openjdk does exist."
        exit -1
    fi
    pushd mmtk-openjdk
    git remote add wenyu https://github.com/wenyuzhao/mmtk-openjdk
    git fetch wenyu
    git checkout -b lxr wenyu/lxr
    popd
fi

if [ ! -d "openjdk" ]; then
    echo "openjdk does exist."
    exit -1
fi
pushd openjdk
git checkout jdk-11.0.15+8-mmtk
popd

if ((probes)); then
    (
        cd probes
    )
fi

sudo add-apt-repository -y ppa:openjdk-r/ppa
sudo apt-get update
sudo apt install -y openjdk-11-jdk

sudo apt-get install -y libx11-dev libxext-dev libxrender-dev libxrandr-dev libxtst-dev libxt-dev
sudo apt-get install -y libcups2-dev
sudo apt-get install -y libasound2-dev