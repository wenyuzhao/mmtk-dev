set -ex

config=$(basename $(dirname $0))
branch=3d213734

build_one() {
    rake jdk:test gc=Immix heap=287M noc1=1 bench=xalan profile=release n=5 features=$2
    rake bench:cp name=$config/$1
}

build_one jdk-$branch lxr_evac,yield_and_roots_timer,work_packet_timer
build_one jdk-ix-$branch ix_defrag,yield_and_roots_timer,work_packet_timer