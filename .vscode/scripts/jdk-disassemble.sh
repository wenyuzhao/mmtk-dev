#!/usr/bin/env bash
set -ex

# Dump asm for function Test.testWriteField in Test.java
CLASS=Test
METHOD=testWriteField

JAVA="./mmtk-openjdk/repos/openjdk/build/linux-x86_64-normal-server-slowdebug/jdk/bin/java"
ARGS="-Xms1G -Xmx1G -XX:+UseThirdPartyHeap"

javac $CLASS.java
LD_LIBRARY_PATH=~ $JAVA $ARGS -XX:+UnlockDiagnosticVMOptions -Xcomp -Xbatch -XX:CompileCommand="compileonly $CLASS $METHOD" -XX:CompileCommand=print,$CLASS.$METHOD -XX:-TieredCompilation -XX:CompileThreshold=1 $CLASS