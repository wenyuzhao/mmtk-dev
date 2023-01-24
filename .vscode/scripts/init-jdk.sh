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

git submodule update --init mmtk-core mmtk-openjdk openjdk # evaluation/probes

if ((lxr)); then
    if [ ! -d "mmtk-core" ]; then
        echo "mmtk-core does exist."
        exit -1
    fi
    pushd mmtk-core
    git remote add wenyu git@github.com:wenyuzhao/mmtk-core.git
    git fetch wenyu
    git checkout -b lxr wenyu/lxr
    popd

    if [ ! -d "mmtk-openjdk" ]; then
        echo "mmtk-openjdk does exist."
        exit -1
    fi
    pushd mmtk-openjdk
    git remote add wenyu git@github.com:wenyuzhao/mmtk-openjdk.git
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
if ((lxr)); then
    git checkout jdk-11.0.15+8-mmtk-lxr
fi
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
# sudo apt-get install -y rr

sudo mkdir -p /usr/share/benchmarks/dacapo
pushd /usr/share/benchmarks/dacapo
sudo wget https://github.com/wenyuzhao/lxr-pldi-2022-artifact/releases/download/_/dacapo-evaluation-git-b00bfa9.jar
sudo wget https://github.com/wenyuzhao/lxr-pldi-2022-artifact/releases/download/_/dacapo-evaluation-git-b00bfa9.zip.aa
sudo wget https://github.com/wenyuzhao/lxr-pldi-2022-artifact/releases/download/_/dacapo-evaluation-git-b00bfa9.zip.ab
sudo wget https://github.com/wenyuzhao/lxr-pldi-2022-artifact/releases/download/_/dacapo-evaluation-git-b00bfa9.zip.ac
sudo wget https://github.com/wenyuzhao/lxr-pldi-2022-artifact/releases/download/_/dacapo-evaluation-git-b00bfa9.zip.ad
sudo bash -c "cat dacapo-evaluation-git-b00bfa9.zip.* > dacapo-evaluation-git-b00bfa9.zip"
sudo mkdir dacapo-evaluation-git-b00bfa9
pushd dacapo-evaluation-git-b00bfa9
sudo unzip ../dacapo-evaluation-git-b00bfa9.zip
popd
sudo rm dacapo-evaluation-git-b00bfa9.zip*
popd