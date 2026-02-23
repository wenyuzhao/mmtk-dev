#!/usr/bin/env bash

mmtk-jdk bench run --config wp/xput-cpus-a-nothp 

mmtk-jdk bench run --config wp/xput-cpus-b-nothp

mmtk-jdk bench run --config wp/util-cpus-nothp