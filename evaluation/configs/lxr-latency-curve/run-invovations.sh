set -ex

run_name=g1-invocations
git=1d0f1098

result_moma=fox.moma
host=$(python -c "import socket; print socket.gethostname()")
_run_id=$host-$(date +%y%m%d-%H%M%S)-$run_name
run_id=${1-$_run_id}
out=~/MMTk-Dev/_latency_logs/$run_id
latency_dump=./evaluation/configs/lxr-latency-curve/latency-dump.py
latency_gen=./evaluation/configs/lxr-latency-curve/latency-gen.py

pushd ~/MMTk-Dev

gc=G1
invocations=$(seq 1 10)
labels=$(seq -f 'G1-%g' 1 10)
ids=
# printf "%02d " {0..10}
for i in $invocations; do
    id=" $gc-default-3x-$i"
    ids+=$id
#     $latency_dump --git $git -gc $gc --out=$out -n 5 -id=$gc-default-3x-$i
#     rsync -azR --no-i-r -h --info=progress2 ~/./MMTk-Dev/_latency_logs $result_moma:/home/wenyuz/
done

# pip3 install hdrhistogram --user
# pip3 install seaborn --user

$latency_gen --dir $out -gc $labels -id $ids --out $run_name

rsync -azR --no-i-r -h --info=progress2 ~/./MMTk-Dev/_latency_logs $result_moma:/home/wenyuz/

popd