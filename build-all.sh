

# make build run TASK=JikesRVM RUN_MACHINE=bear.moma GC=FastAdaptiveG1BarrierBaseline
# make build run TASK=JikesRVM RUN_MACHINE=bear.moma GC=FastAdaptiveG1BarrierSATBCond
# make build run TASK=JikesRVM RUN_MACHINE=bear.moma GC=FastAdaptiveG1BarrierSATBUncond
# make build run TASK=JikesRVM RUN_MACHINE=bear.moma GC=FastAdaptiveG1BarrierCardMarking
# make build run TASK=JikesRVM RUN_MACHINE=bear.moma GC=FastAdaptiveG1BarrierXOR
# make build run TASK=JikesRVM RUN_MACHINE=bear.moma GC=FastAdaptiveG1BarrierAll

# make build run TASK=JikesRVM RUN_MACHINE=fisher.moma GC=FastAdaptiveG1BarrierBaseline
# make build run TASK=JikesRVM RUN_MACHINE=fisher.moma GC=FastAdaptiveG1BarrierSATBCond
# make build run TASK=JikesRVM RUN_MACHINE=fisher.moma GC=FastAdaptiveG1BarrierSATBUncond
# make build run TASK=JikesRVM RUN_MACHINE=fisher.moma GC=FastAdaptiveG1BarrierCardMarking
# make build run TASK=JikesRVM RUN_MACHINE=fisher.moma GC=FastAdaptiveG1BarrierXOR
# make build run TASK=JikesRVM RUN_MACHINE=fisher.moma GC=FastAdaptiveG1BarrierAll

make build run TASK=JikesRVM RUN_MACHINE=ferret.moma GC=FastAdaptiveG1PauseAnalysis_STWMark_NoRemSet_NonGen
make build run TASK=JikesRVM RUN_MACHINE=ferret.moma GC=FastAdaptiveG1PauseAnalysis_STWMark_RemSet_NonGen
make build run TASK=JikesRVM RUN_MACHINE=ferret.moma GC=FastAdaptiveG1PauseAnalysis_STWMark_RemSet_Gen
make build run TASK=JikesRVM RUN_MACHINE=ferret.moma GC=FastAdaptiveG1PauseAnalysis_ConcMark_NoRemSet_NonGen
make build run TASK=JikesRVM RUN_MACHINE=ferret.moma GC=FastAdaptiveG1PauseAnalysis_ConcMark_RemSet_NonGen_Predictor
make build run TASK=JikesRVM RUN_MACHINE=ferret.moma GC=FastAdaptiveG1PauseAnalysis_ConcMark_RemSet_Gen_Predictor