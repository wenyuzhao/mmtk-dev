#!/usr/bin/env bash

sudo add-apt-repository ppa:openjdk-r/ppa -y
sudo apt update && apt upgrade -y
sudo apt install -y build-essential gdb libx11-dev libxext-dev libxrender-dev libxrandr-dev libxtst-dev libxt-dev libcups2-dev libasound2-dev default-jdk gcc-multilib libpfm4-dev gcc-multilib
git submodule update --init --recursive
git lfs install
git lfs pull
rustup toolchain add nightly-2021-05-12