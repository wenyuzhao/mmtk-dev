#!/usr/bin/env bash
set -ex

source $(dirname $0)/../utils.sh

render_config


export PATH=$HOME/.cargo/bin:$PATH

# build_one jdk-lxr-stw-submit-$branch lxr

# NURSERY_RATIO=1 build_one jdk-lxr-$branch lxr
# build_one jdk-rcix-$branch rc_immix
build_one jdk-ix-$branch ix_defrag
# OPPORTUNISTIC_EVAC=1 OPPORTUNISTIC_EVAC_THRESHOLD=50 TRACE_THRESHOLD=30 MAX_MATURE_DEFRAG_PERCENT=15 INCS_LIMIT=10000 build_one jdk-lxr-$branch lxr,lxr_heap_health_guided_gc
# MAX_MATURE_DEFRAG_PERCENT=20 OPPORTUNISTIC_EVAC=1 OPPORTUNISTIC_EVAC_THRESHOLD=50 build_one jdk-lxr-$branch lxr,lxr_heap_health_guided_gc
# MAX_MATURE_DEFRAG_PERCENT=20 OPPORTUNISTIC_EVAC=1 OPPORTUNISTIC_EVAC_THRESHOLD=50 build_one jdk-lxr-stw-$branch lxr_evac,lxr_heap_health_guided_gc

# NURSERY_RATIO=1 build_one jdk-lxr-stw-old-$branch lxr_evac

# for i in $(seq 3 9); do
#     build_one jdk-lock-$i-$branch lxr_evac,mmtk/lxr_lock_$i
# done

# build_one jdk-block-64k-$branch lxr_evac,mmtk/lxr_block_64k
# build_one jdk-block-128k-$branch lxr_evac,mmtk/lxr_block_128k
# build_one jdk-block-256k-$branch lxr_evac,mmtk/lxr_block_256k
# build_one jdk-block-512k-$branch lxr_evac,mmtk/lxr_block_512k
# build_one jdk-block-1m-$branch lxr_evac,mmtk/lxr_block_1m


============================ MMTk Statistics Totals ============================
 - FlushMatureEvacRemsets              total=         310045    min=      3767    max=          93807    avg=       23849.62    count=        13
 - RCReleaseUnallocatedNurseryBlocks   total=         432352    min=       150    max=          10480    avg=        1091.80    count=       396
 - RCSweepNurseryBlocks                total=      529067416    min=        80    max=         134655    avg=        6958.48    count=     76032
 - PrepareChunk                        total=        4569322    min=      3347    max=          31008    avg=       10651.10    count=       429
 - SweepDeadCyclesChunk                total=       78169017    min=     42310    max=        4841020    avg=      182212.16    count=       429
 - MatureSweeping                      total=        2806373    min=    185301    max=         249792    avg=      215874.85    count=        13
 - SelectDefragBlocksInChunk           total=       11350994    min=      8556    max=         262235    avg=       26459.19    count=       429
 - RCReleaseMatureLOS                  total=        3825909    min=       391    max=         110980    avg=        9661.39    count=       396
 - RCSweepMatureLOS                    total=         700875    min=     39886    max=          79150    avg=       53913.46    count=        13
 - EndOfGC                             total=       62277480    min=     65244    max=         373997    avg=      157266.36    count=       396
 - EvacuateMatureObjects               total=       74032796    min=       581    max=        1045917    avg=       35592.69    count=      2080
 - Prepare                             total=        2293885    min=       711    max=          11472    avg=        5792.64    count=       396
 - Release                             total=        6340015    min=      3557    max=          39695    avg=       16010.14    count=       396
 - ScanStackRoot                       total=      922809819    min=       561    max=         612478    avg=       71122.14    count=     12975
 - ScheduleCollection                  total=       25836753    min=     20058    max=        2384457    avg=       65244.33    count=       396
 - StopMutators                        total=      211075845    min=    190701    max=        2361263    avg=      533019.81    count=       396
 - ImmixConcurrentTraceObjects         total=     1815734948    min=       100    max=        7377774    avg=       10932.63    count=    166084
 - LXRStopTheWorldProcessEdges         total=      129207797    min=        90    max=         939856    avg=        7965.96    count=     16220
 - ProcessModBufSATB                   total=        3457955    min=       251    max=         723768    avg=        5532.73    count=       625
 - ProcessDecs                         total=      503598982    min=       160    max=        6617767    avg=       14755.32    count=     34130
 - ProcessIncs                         total=      936769223    min=       160    max=       14971598    avg=       26059.01    count=     35948
 - RCImmixCollectRootEdges             total=       18134682    min=       100    max=          39705    avg=         685.00    count=     26474
 - SweepBlocksAfterDecs                total=       25441024    min=        80    max=          53982    avg=        1338.44    count=     19008
 - ScanAOTLoaderRoots                  total=        1196415    min=       291    max=          40116    avg=        3021.25    count=       396
 - ScanClassLoaderDataGraphRoots       total=       52476569    min=     32011    max=         323311    avg=      132516.59    count=       396
 - ScanCodeCacheRoots                  total=      152536840    min=    220086    max=         556311    avg=      385194.04    count=       396
 - ScanJNIHandlesRoots                 total=        7578823    min=       781    max=         209266    avg=       19138.44    count=       396
 - ScanJvmtiExportRoots                total=        1370467    min=       380    max=          44754    avg=        3460.78    count=       396
 - ScanManagementRoots                 total=        6254765    min=       841    max=         217651    avg=       15794.86    count=       396
 - ScanObjectSynchronizerRoots         total=        1389823    min=       410    max=          44805    avg=        3509.65    count=       396
 - ScanStringTableRoots                total=       43587739    min=     30057    max=         334052    avg=      110070.05    count=       396
 - ScanSystemDictionaryRoots           total=       13214418    min=      2474    max=         222931    avg=       33369.74    count=       396
 - ScanUniverseRoots                   total=       17305019    min=      1232    max=         277395    avg=       43699.54    count=       396
 - ScanVMThreadRoots                   total=        2982546    min=      1694    max=          77677    avg=        7531.68    count=       396
 - ScanWeakProcessorRoots              total=       11116685    min=      5881    max=         220897    avg=       28072.44    count=       396
SUM: 5679253616 ns