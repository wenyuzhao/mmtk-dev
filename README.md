
# Getting Started

1. Open with GitHub Codespace or `git clone https://github.com/wenyuzhao/MMTk-Dev.git --recursive`

## OpenJDK

1. `rake jdk:config` -- _Note: this only needs to run once._
2. `rake jdk:test gc=semispace heap=100M bench=xalan`

## JikesRVM

1. `rake jks:build profile=RBaseBaseSemiSpace `
2. `rake jks:test profile=RBaseBaseSemiSpace heap=100M bench=xalan`

# V8

...WIP