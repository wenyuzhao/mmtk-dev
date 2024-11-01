#!/usr/bin/env bash

mmtk-jdk bench run --config wp/util-cpus-a --invocations 5
mmtk-jdk bench run --config wp/util-cpus-b --invocations 5
mmtk-jdk bench run --config wp/util-cpus-a --invocations 5
mmtk-jdk bench run --config wp/util-cpus-b --invocations 5