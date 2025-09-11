#!/usr/bin/env bash

# mmtk-jdk bench run --config lxr-prod/xput-nothp # 44

# mmtk-jdk bench run --config lxr-prod/xput-nothp-jdk21-fix # 2

# mmtk-jdk bench run --config lxr-prod/lbo-nothp-jdk21-fix # 12

# mmtk-jdk bench run --config lxr-pldi/xput-nothp # 44

# mmtk-jdk bench run --config lxr-prod/xput-nothp-jdk2124 # 184

# mmtk-jdk bench run --config lxr-pldi/xput-6x-nothp # 34

# mmtk-jdk bench run --config wp/xput-1.5x-g121-fix

# mmtk-jdk bench run --config wp/xput-2x-g121-fix

# mmtk-jdk bench run --config lxr-pldi/xput-1.3x-nothp

# [wp]xput-nothp-bear-2025-09-08-Mon-105455
# [wp]xput-nothp-2-bear-2025-09-09-Tue-032650
# [wp]xput-nothp-3-bear-2025-09-09-Tue-134216

# ^[wp]xput-nothp-bear-2025-09-08-Mon-105455^[wp]xput-nothp-2-bear-2025-09-09-Tue-032650^[wp]xput-nothp-3-bear-2025-09-09-Tue-134216
# mmtk-jdk bench run --config wp/xput-nothp-3

# mmtk-jdk bench run --config lxr-prod/lbo-nothp-2 --invocations 5 # 16

# mmtk-jdk bench run --config wp/xput-1.5x-nothp-xalan-ixp

# mmtk-jdk bench run --config lxr-prod/weak-processor-nothp # 66

# mmtk-jdk bench run --config lxr-prod/block-alloc-nothp # 66

mmtk-jdk bench run --config lxr-prod/cm-rate-nothp --invocations 10