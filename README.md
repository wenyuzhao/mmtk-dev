
# Getting Started

1. `git clone https://github.com/wenyuzhao/MMTk-Dev.git --recursive`
2. Run `rake init` once to initialize the repo.

## Instructions

* [OpenJDK](#openjdk)
  * [Config](#config-once)
  * [Build and run DaCapo](#build-and-run-dacapo-chopin-benchmark)
  * [Launch GDB](#launch-gdb)
  * [Launch GDB](#benchmarking)
* [JikesRVM](#jikesrvm)
* [V8](#v8)

# OpenJDK

## Config (once)

`rake jdk:config` -- _Note: this only needs to run once._

* Config for release build: `rake jdk:config release=1`

## Build and run DaCapo (chopin) benchmark

_Please do the config step above once before building._

`rake jdk:test gc=SemiSpace heap=100M bench=xalan`

* Run with release build: `rake jdk:test gc=SemiSpace heap=100M bench=xalan release=1`
* Run with multiple iterations: `rake jdk:test gc=SemiSpace heap=100M bench=xalan n=5`
* Disable C1: `rake jdk:test gc=SemiSpace heap=100M bench=xalan noc1=1`
* Interpreter only: `rake jdk:test gc=SemiSpace heap=100M bench=xalan int=1`
* Fix mutator threads: `rake jdk:test gc=SemiSpace heap=100M bench=xalan t=10`
* Fix GC worker threads: `rake jdk:test gc=SemiSpace heap=100M bench=xalan threads=10`

## Launch GDB

`rake jdk:gdb gc=SemiSpace heap=100M bench=xalan`


# Benchmarking

WIP

# JikesRVM

1. `rake jks:build profile=RBaseBaseSemiSpace`
2. `rake jks:test profile=RBaseBaseSemiSpace heap=100M bench=xalan`
    * Run with multiple iterations: `rake jks:test profile=RBaseBaseSemiSpace heap=100M bench=xalan n=5`

# V8

...WIP
