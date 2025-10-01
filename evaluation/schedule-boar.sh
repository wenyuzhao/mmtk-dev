#!/usr/bin/env bash

# mmtk-jdk bench run --config lxr-prod/latency-nothp # 16

# mmtk-jdk bench run --config lxr-prod/lbo-nothp # 16

# [wp]xput-1.5x-nothp-boar-2025-09-09-Tue-030038

# mmtk-jdk bench run --config wp/xput-1.5x-nothp-2

# mmtk-jdk bench run --config lxr-prod/lbo-nothp-2 --invocations 5

# mmtk-jdk bench run --config wp/util-nothp --invocations 3

# mmtk-jdk bench run --config wp/util-nothp-2 --invocations 10

# mmtk-jdk bench run --config lxr-prod/lbo-nothp-3 --invocations 5

# mmtk-jdk bench run --config lxr-prod/xput-nothp-2 --invocations 10

# mmtk-jdk bench run --config lxr-prod/latency-nothp-2 --invocations 10

# mmtk-jdk bench run --config lxr-prod/cm-rate-nothp --invocations 10 # 184

# mmtk-jdk bench run --config wp/util-nothp --invocations 3

mmtk-jdk bench run --config lxr-prod/block-alloc-weak-proc-nothp --invocations 10
