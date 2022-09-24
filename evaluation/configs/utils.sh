render_config() {
    cat $config_dir/config.yml | sed "s/{config}/$config/" | sed "s/{git}/$branch/" | tee $config_dir/_config.yml
}