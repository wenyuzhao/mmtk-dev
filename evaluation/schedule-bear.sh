#!/usr/bin/env bash

mmtk-jdk bench run --config lxr-prod/xput-nothp # 44

mmtk-jdk bench run --config lxr-prod/xput-nothp-jdk21-fix # 2

mmtk-jdk bench run --config lxr-prod/lbo-nothp-jdk21-fix # 12

mmtk-jdk bench run --config lxr-pldi/xput-nothp # 44

mmtk-jdk bench run --config lxr-pldi/xput-6x-nothp # 34

mmtk-jdk bench run --config lxr-prod/cm-rate-nothp # 184

mmtk-jdk bench run --config lxr-prod/block-alloc-nothp # 66

mmtk-jdk bench run --config wp/xput-1.5x-g121-fix

mmtk-jdk bench run --config wp/xput-2x-g121-fix