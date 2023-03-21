#!/usr/bin/env bash

set -e

declare -r script_dir=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )

declare lxr=0
declare install_pkgs=0

while [[ $# -gt 0 ]]; do
  case $1 in
    --lxr)
      lxr=1
      shift
      ;;
    --pkgs|--install-pkgs|--install-packages)
      install_pkgs=1
      shift
      ;;
    *)
      shift
      ;;
  esac
done

echo "[Initialize mmtk-core]"
$script_dir/init/mmtk.sh
if ((lxr)); then
    $script_dir/init/mmtk.sh --lxr
fi

echo "[Initialize mmtk-openjdk and openjdk]"
$script_dir/init/jdk.sh
if ((lxr)); then
    $script_dir/init/jdk.sh --lxr
fi

echo "[Initialize dacapo]"
$script_dir/init/dacapo.sh

echo "[Initialize probes]"
$script_dir/init/probes.sh

if ((install_pkgs)); then
    echo "[Install packages]"
    $script_dir/init/install-packages.sh
fi