#!/usr/bin/env bash
set -ex

# Dump asm for function Test.testWriteField in Test.java
CLASS=Test
METHOD=testObjectClone
export MMTK_PLAN=Immix

JAVA="./mmtk-openjdk/repos/openjdk/build/linux-x86_64-normal-server-release/jdk/bin/java"
# JAVA="./evaluation/build/jdk-mmtk-gencopy-object-barrier-testglobal-1/jdk/bin/java"
ARGS="-Xms1G -Xmx1G -XX:+UseThirdPartyHeap"
export PERF_EVENTS=

javac $CLASS.java
LD_LIBRARY_PATH=~ $JAVA $ARGS -XX:+UnlockDiagnosticVMOptions -Xcomp -Xbatch -XX:CompileCommand="compileonly Object clone" -XX:CompileCommand="compileonly $CLASS $METHOD" -XX:CompileCommand=print,$CLASS.$METHOD -XX:-TieredCompilation -XX:CompileThreshold=1 $CLASS