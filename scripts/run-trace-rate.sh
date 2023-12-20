bench=h2
heap='16G'

# Baseline
# ./run-jdk --gc=LXR --bench=h2 --heap=16G -n 1 -xbr --features mmtk/lxr_simple_satb_trigger,mmtk/lxr_no_mature_defrag,mmtk/measure_trace_rate -v 3 -s large &> tr-base.log



# ./run-jdk --gc=LXR --bench=h2 --heap=16G -n 1 -xbr --features mmtk/lxr_simple_satb_trigger,mmtk/lxr_no_mature_defrag,mmtk/measure_trace_rate,mmtk/opt_attempt_mark -v 3 -s large &> tr-mark.log


# ./run-jdk --gc=LXR --bench=h2 --heap=16G -n 1 -xbr --features mmtk/lxr_simple_satb_trigger,mmtk/lxr_no_mature_defrag,mmtk/measure_trace_rate,mmtk/opt_attempt_mark,mmtk/opt_space_check -v 3 -s large &> tr-space.log


# ./run-jdk --gc=LXR --bench=h2 --heap=16G -n 1 -xbr --features mmtk/lxr_simple_satb_trigger,mmtk/lxr_no_mature_defrag,mmtk/measure_trace_rate,mmtk/opt_attempt_mark,mmtk/opt_space_check,mmtk/no_dyn_dispatch -v 3 -s large &> tr-dyn.log


./run-jdk --gc=LXR --bench=h2 --heap=16G -n 1 -xbr --features mmtk/lxr_simple_satb_trigger,mmtk/lxr_no_mature_defrag,mmtk/measure_trace_rate,mmtk/opt_attempt_mark,mmtk/opt_space_check,mmtk/no_dyn_dispatch,mmtk/fast_rc_check -v 3 -s large &> tr-e.log