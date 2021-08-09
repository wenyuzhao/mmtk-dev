#!/usr/bin/env bash

sudo apt update && apt upgrade -y
sudo apt install -y build-essential gdb libx11-dev libxext-dev libxrender-dev libxrandr-dev libxtst-dev libxt-dev libcups2-dev libasound2-dev
git submodule update --init --recursive
rustup toolchain add nightly-2021-05-12