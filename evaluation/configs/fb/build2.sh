set -ex

config=$(basename $(dirname $0))
branch=3d213734

build_one() {
    rake jdk:test gc=Immix heap=287M noc1=1 bench=xalan profile=release n=5 features=$2
    rake bench:cp name=$config/$1
}

BARRIER=FieldBarrier build_one jdk-$branch barrier_measurement,ix_defrag

