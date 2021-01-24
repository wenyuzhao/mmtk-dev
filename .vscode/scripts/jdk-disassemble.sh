#!/usr/bin/env bash 
set -ex
JAVA="./mmtk-openjdk/repos/openjdk/build/linux-x86_64-normal-server-slowdebug/jdk/bin/java"
ARGS="-Xms1G -Xmx1G -XX:+UseThirdPartyHeap"

javac Test.java

LD_LIBRARY_PATH=/home/wenyuz/ $JAVA $ARGS -XX:+UnlockDiagnosticVMOptions -Xcomp -Xbatch -XX:CompileCommand="compileonly Test testWriteField" '-XX:CompileCommand=print,Test.testWriteField' -XX:-TieredCompilation -XX:+PrintCompilation -XX:CompileThreshold=1 -XX:+PrintAssembly  Test > x.log