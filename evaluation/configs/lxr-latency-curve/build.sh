set -ex

config=$(basename $(dirname $0))
pushd ~/MMTk-Dev/mmtk-core
branch=$(git rev-parse --short HEAD)
popd

build_one() {
    rake jdk:test gc=Immix heap=287M noc1=1 bench=xalan profile=release n=5 features=$2
    rake bench:cp name=$config/$1
}

build_one jdk-$branch lxr
