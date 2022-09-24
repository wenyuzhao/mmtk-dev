#!/usr/bin/env bash
set -ex

config=$(basename $(dirname $0))

pkill -f java -u wenyuz -9

pushd ~/MMTk-Dev

# Build master
pushd ~/MMTk-Dev/mmtk-core
git checkout master-cp
branch=${1:-$(git rev-parse --short HEAD)}
echo "compressed-ptr master branch $branch"
popd
pushd ~/MMTk-Dev/mmtk-openjdk
git checkout master
popd
./run-jdk.py --gc=SemiSpace --heap=300M --bench=lusearch --build --profile=release
cp -r ./openjdk/build/linux-x86_64-normal-server-release ~/MMTk-Dev/evaluation/builds/jdk-mmtk-master-$branch

# Build compressed-ptr
# pushd ~/MMTk-Dev/mmtk-core
# git checkout compressed-ptr
# branch=${1:-$(git rev-parse --short HEAD)}
# echo "compressed-ptr branch $branch"
# popd
# pushd ~/MMTk-Dev/mmtk-openjdk
# git checkout compressed-ptr
# popd
# ./run-jdk.py --gc=SemiSpace --heap=300M --bench=lusearch --build --profile=release
# cp -r ./openjdk/build/linux-x86_64-normal-server-release ~/MMTk-Dev/evaluation/builds/jdk-mmtk-compressed-ptr-$branch

popd