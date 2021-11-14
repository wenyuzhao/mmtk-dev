set -ex

branch=88cd1e86

build_one() {
    rake jdk:test gc=Immix heap=287M noc1=1 bench=xalan profile=release n=5 features=$2
    rake bench:cp name=ix-xput/$1
}

build_one jdk-$branch lxr_evac,work_packet_timer
build_one jdk-no-wp-timer-$branch lxr_evac
build_one jdk-128k-$branch lxr_evac,mmtk/lxr_block_128k,mmtk/work_packet_timer