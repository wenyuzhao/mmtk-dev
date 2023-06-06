#!/usr/bin/env bash

set -e

declare -r dacapo_version=04132797
declare dacapo_path="/usr/share/benchmarks/dacapo"

while [[ "$#" -gt 0 ]]; do
    opt="$1"; shift;
    case "$opt" in
        --path)
            dacapo_path=$1
            shift
            ;;
        *)
            shift
            ;;
    esac
done


declare -r download_url_base=https://github.com/wenyuzhao/lxr-pldi-2022-artifact/releases/download/_
declare -r dacapo_name=dacapo-evaluation-git-$dacapo_version

# if [ -d "$dacapo_path" ]; then
#     echo "$dacapo_path already exists."
#     exit 0
# fi

sudo mkdir -p $dacapo_path/$dacapo_name

pushd $dacapo_path
    sudo wget $download_url_base/$dacapo_name.jar
    sudo wget $download_url_base/$dacapo_name.zip.aa
    sudo wget $download_url_base/$dacapo_name.zip.ab
    sudo wget $download_url_base/$dacapo_name.zip.ac
    sudo wget $download_url_base/$dacapo_name.zip.ad
    sudo bash -c "cat $dacapo_name.zip.* > $dacapo_name.zip"
    pushd $dacapo_name
        sudo unzip ../$dacapo_name.zip
    popd
    sudo rm $dacapo_name.zip*
popd