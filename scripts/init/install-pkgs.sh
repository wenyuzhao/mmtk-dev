#!/usr/bin/env bash

set -ex

curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh -s -- -y

sudo apt-get update -y
sudo apt-get -y install build-essential libx11-dev libxext-dev libxrender-dev libxtst-dev libxt-dev libcups2-dev libasound2-dev libxrandr-dev
