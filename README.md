
# Clone this repo

1. `git clone https://github.com/wenyuzhao/MMTk-Dev.git --recursive`
2. `cd MMTk-Dev`

# OpenJDK: Quick Start

1. `make vm=jdk config` -- _Note: this only needs to run once._
2. `make vm=jdk build run gc=semispace benchmark=xalan`

### Release Build

1. `make vm=jdk config profile=release`
2. `make vm=jdk build run profile=release gc=semispace benchmark=xalan`

### Run _mmtk-core_ Pre-submission CI

* `make vm=jdk run-ci-tests`

# JikesRVM: Quick Start

1. `make vm=jikes config` -- _Note: this only needs to run once._
1. `make vm=jikes build test profile=RBaseBaseSemiSpace benchmark=xalan`

# V8: Quick Start

1. `make vm=v8 setup` -- _Note: this only needs to run once._
1. `make vm=v8 build test`