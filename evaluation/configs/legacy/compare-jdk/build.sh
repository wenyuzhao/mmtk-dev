#!/usr/bin/env bash
set -x

config=$(basename $(dirname $0))

pkill -f java -u wenyuz -9

pushd ~/MMTk-Dev

# Build jdk-11.0.11+6
pushd ~/MMTk-Dev/mmtk-core
git checkout 0babba20290d3c4e4cdb2a83284aa7204c9a23cc
popd
pushd ~/MMTk-Dev/mmtk-openjdk
git checkout 167058d996b050859a109ab16829231b3a9f16e4
popd
pushd ~/MMTk-Dev/openjdk
git checkout 67d5d2b16aacb2ea948552fab2323ebd0abbe924
popd
pushd ~/MMTk-Dev/openjdk/build/linux-x86_64-normal-server-release
make reconfigure
popd
./run-jdk.py --gc=SemiSpace --heap=300M --bench=lusearch --build --profile=release
cp -r ./openjdk/build/linux-x86_64-normal-server-release ~/MMTk-Dev/evaluation/builds/jdk-mmtk-11116

# Build master
pushd ~/MMTk-Dev/openjdk
git checkout ca90b43f0f51d9ddf754e6ab134c5030cf54118b
popd
pushd ~/MMTk-Dev/openjdk/build/linux-x86_64-normal-server-release
make reconfigure
popd
./run-jdk.py --gc=SemiSpace --heap=300M --bench=lusearch --build --profile=release
cp -r ./openjdk/build/linux-x86_64-normal-server-release ~/MMTk-Dev/evaluation/builds/jdk-mmtk-11158

popd