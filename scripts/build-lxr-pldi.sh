set -ex

GC_FEATURES=lxr,lxr_heap_health_guided_gc \
TRACE_THRESHOLD2=10 LOCK_FREE_BLOCKS=32 MAX_SURVIVAL_MB=256 SURVIVAL_PREDICTOR_WEIGHTED=1 \
./run-jdk.py  --gc=Immix --heap=300M --bench=lusearch --build --profile=release --no-c1 --jdk-args="-XX:+UnlockDiagnosticVMOptions -XX:-InlineObjectCopy -XX:-ClassUnloading -XX:-ClassUnloadingWithConcurrentMark -XX:-RegisterReferences"