#!/usr/bin/env bash

mmtk-jdk bench run --config wp/xput-cpus-a --invocations 5
mmtk-jdk bench run --config wp/xput-cpus-b --invocations 5
# mmtk-jdk bench run --config wp/xput-cpus-a --invocations 5
# mmtk-jdk bench run --config wp/xput-cpus-b --invocations 5