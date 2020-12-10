
# Quick Start

1. `git clone https://github.com/wenyuzhao/MMTk-Dev.git --recursive`
2. `cd MMTk-Dev`
3. `make config`
   * _Note: this only needs to run once._
4. `make build run gc=semispace benchmark=xalan`

# Release Build

1. `make config profile=release`
2. `make build run profile=release gc=semispace benchmark=xalan`

# TODO

* Add JikesRVM and V8 binding repos