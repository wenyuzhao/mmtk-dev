set -ex

config=lxr-satb-time
branch=3641537b

build_one() {
    rake jdk:test gc=Immix heap=287M noc1=1 bench=xalan profile=release n=5 features=$2
    rake bench:cp name=$config/$1
}

build_one jdk-$branch lxr_evac,lxr_cm,work_packet_timer,satb_timer