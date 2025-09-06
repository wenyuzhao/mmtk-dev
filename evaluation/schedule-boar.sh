#!/usr/bin/env bash

mmtk-jdk bench run --config lxr-prod/latency-nothp # 16

mmtk-jdk bench run --config lxr-prod/lbo-nothp # 16

mmtk-jdk bench run --config lxr-pldi/xput-1.3x-nothp # 264

mmtk-jdk bench run --config lxr-prod/weak-processor-nothp # 66

mmtk-jdk bench run --config wp/xput-nothp
