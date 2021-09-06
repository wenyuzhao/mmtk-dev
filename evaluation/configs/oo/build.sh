#!/usr/bin/env bash
set -ex
MMTK_DEV_DIR=~/MMTk-Dev
CONFIG_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"
# rake jdk:test gc=immix heap=200M bench=xalan noc1=1 profile=release n=3
# cp -r $MMTK_DEV_DIR/mmtk-openjdk/repos/openjdk/build/linux-x86_64-normal-server-release $CONFIG_DIR/jdk-immix-cm-nobarrier
# FLB_KIND=IU rake jdk:test gc=immix heap=200M bench=xalan noc1=1 profile=release n=3
# cp -r $MMTK_DEV_DIR/mmtk-openjdk/repos/openjdk/build/linux-x86_64-normal-server-release $CONFIG_DIR/jdk-immix-cm-fieldlogging-iu
rake jdk:test gc=gencopy heap=200M bench=batik noc1=1 profile=release
cp -r $MMTK_DEV_DIR/mmtk-openjdk/repos/openjdk/build/linux-x86_64-normal-server-release $CONFIG_DIR/jdk-immix-cm-fieldlogging-satb

