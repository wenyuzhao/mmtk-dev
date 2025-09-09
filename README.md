Configs, scripts, and tools for my MMTk-related performance evaluation.

# Getting Started

1. `git clone https://github.com/wenyuzhao/MMTk-Dev.git --recursive`
2. Run `rake init` once to initialize the repo.

## OpenJDK

1. `rake jdk:config` -- _Note: this only needs to run once._
2. `rake jdk:test gc=SemiSpace heap=100M bench=xalan`

## JikesRVM

1. `rake jks:build profile=RBaseBaseSemiSpace `
2. `rake jks:test profile=RBaseBaseSemiSpace heap=100M bench=xalan`

# V8

...WIP
