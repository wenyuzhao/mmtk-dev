set -ex

run_name=shenandoah-mutators
git=1d0f1098

result_moma=fox.moma
host=$(python -c "import socket; print socket.gethostname()")
_run_id=$host-$(date +%y%m%d-%H%M%S)-$run_name
run_id=${1-$_run_id}
out=~/MMTk-Dev/_latency_logs/$run_id
latency_dump=./evaluation/configs/lxr-latency-curve/latency-dump.py
latency_gen=./evaluation/configs/lxr-latency-curve/latency-gen.py

pushd ~/MMTk-Dev

gc=Shenandoah
ts="3 6 12 24"
labels=
ids=

for t in $ts; do
    echo $t;
    id=$gc-default-3x-t$t
    labels+=" $gc-t$t"
    ids+=" $id"
    $latency_dump --git $git -gc $gc -t $t --out=$out -id=$id
    rsync -azR --no-i-r -h --info=progress2 ~/./MMTk-Dev/_latency_logs $result_moma:/home/wenyuz/
done

# pip3 install hdrhistogram --user
# pip3 install seaborn --user

$latency_gen --dir $out -gc $labels -id $ids --out shenandoah-mutators.metered --type metered
$latency_gen --dir $out -gc $labels -id $ids --out shenandoah-mutators.simple --type simple
rsync -azR --no-i-r -h --info=progress2 ~/./MMTk-Dev/_latency_logs $result_moma:/home/wenyuz/

popd