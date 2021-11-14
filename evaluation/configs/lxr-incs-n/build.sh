set -ex

config=lxr-incs-n
branch=a36ff5bc

build_one() {
    rake jdk:test gc=Immix heap=287M noc1=1 bench=xalan profile=release n=5 features=$2
    rake bench:cp name=$config/$1
}

build_one jdk-$branch lxr_evac
build_one jdk-ins-$branch lxr_evac,instrumentation