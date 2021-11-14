set -ex

branch=b8d7e549

build_one() {
    rake jdk:test gc=Immix heap=287M noc1=1 bench=xalan profile=release n=5 features=lxr_evac,mmtk/lxr_block_$1 NURSERY_BLOCKS=$2 LOCK_FREE_BLOCKS=$3
    rake bench:cp name=lxr-block-size/jdk-$1-$branch
}

# build_one 16k 2048 32
# build_one 32k 1024 32
# build_one 64k 512 32
# build_one 128k 256 32
# build_one 256k 128 32
# build_one 512k 64 2
# build_one 1m 32 16

build_one_fix_los() {
    rake jdk:test gc=Immix heap=287M noc1=1 bench=xalan profile=release n=5 features=lxr_evac,mmtk/lxr_los_16k,mmtk/lxr_block_$1
    rake bench:cp name=lxr-block-size/jdk-los16k-$1-$branch
}

build_one_fix_los 16k 2048 32
build_one_fix_los 32k 1024 32
build_one_fix_los 64k 512 32
build_one_fix_los 128k 32
build_one_fix_los 256k 32
# build_one_fix_los 512k 16
# build_one_fix_los 1m 16