make build run RUN_MACHINE=bear.moma GC=FastAdaptiveG1BarrierBaseline
make build run RUN_MACHINE=bear.moma GC=FastAdaptiveG1BarrierSATBCond
make build run RUN_MACHINE=bear.moma GC=FastAdaptiveG1BarrierSATBUncond
make build run RUN_MACHINE=bear.moma GC=FastAdaptiveG1BarrierCardMarking
make build run RUN_MACHINE=bear.moma GC=FastAdaptiveG1BarrierXOR
make build run RUN_MACHINE=bear.moma GC=FastAdaptiveG1BarrierAll

make build run RUN_MACHINE=shrew.moma GC=FastAdaptiveG1BarrierBaseline
make build run RUN_MACHINE=shrew.moma GC=FastAdaptiveG1BarrierSATBCond
make build run RUN_MACHINE=shrew.moma GC=FastAdaptiveG1BarrierSATBUncond
make build run RUN_MACHINE=shrew.moma GC=FastAdaptiveG1BarrierCardMarking
make build run RUN_MACHINE=shrew.moma GC=FastAdaptiveG1BarrierXOR
make build run RUN_MACHINE=shrew.moma GC=FastAdaptiveG1BarrierAll