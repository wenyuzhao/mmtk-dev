config_dir=$(dirname $0)
config=$(basename $config_dir)
pushd ~/MMTk-Dev/mmtk-core
branch=$(git rev-parse --short HEAD)
popd

render_config() {
    cat $config_dir/config.yml | sed "s/{config}/$config/" | sed "s/{git}/$branch/" | tee $config_dir/_config.yml
}

build_one() {
    rake jdk:test gc=Immix heap=287M noc1=1 bench=xalan profile=release n=5 features=$2
    rake bench:cp name=$config/$1
}
