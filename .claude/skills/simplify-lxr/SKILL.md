---
name: simplify-lxr
description: Simplify LXR GC for upstreaming
disable-model-invocation: true
---

# Simplify LXR GC for upstreaming

`lxr-x/simplified` branch in mmtk-core and `lxr-x/jdk21-simplified` branch in mmtk-openjdk contain the implementation of the LXR garbage collector.

`lxr-x/simplified` in mmtk-core is based on tag `v0.32.0`
`lxr-x/jdk21-simplified` in mmtk-openjdk is based on tag `v0.32.0-jdk-21`

Both branches contains:
* The core LXR GC algorithm
* Additional performance optimizations
* Changes to the MMTk interface and other components of MMTk
* Changes to support additional fetures, e.g. weak refs and class unloading
* Custom instrumentation and logging code
* Changes to the other GCs in MMTk
* Other stale dead code

You need to work on the `lxr-x/simplified` and `lxr-x/jdk21-simplified`.

You need to simplify the two branches so that the user can easily upstream a simplified version of LXR GC easily, although the performance may not be as good as the original one.

Assume the upstream is at `v0.32.0` and `v0.32.0-jdk-21`.

# Compare and understand git diff

Generate git diff for both mmtk-core and mmtk-openjdk, and understand the changes in the two branches.

# Start a small refactoring/simplification task

The diff may be over 8K LOC, You can't do all the changes in one go.
Only pick a few components/aspects of the codebase that can be simplified/refactored, and perform this task.

Enter plan mode, and preset a plan before proceeding with the task.

# What can be simplified/removed

* Additional performance optimizations
    * e.g., Fast primitive array scanning, vm_map_32
* Changes to the other GCs in MMTk
    * Unless they are part of the necessary MMTk interface change
* Changes to support additional fetures, e.g. weak refs and class unloading
* Custom instrumentation and logging code
* Other stale dead code or comments that is not in upstream

# What can be refactored

* Move LXR-related code, e.g. work packets and counters, to mmtk-core/src/plan/lxr
* Refactor MMTk interface changes to make it more reasonable

# What cannot change

* Necessary changes to the MMTk interface
* The core LXR algorithm
* Keep the following features: lxr_no_evac, lxr_no_cm, lxr_no_lazy, lxr_stw, lxr_no_nursery_evac, lxr_no_mature_evac
* `panic = "abort"` in mmtk-openjdk/mmtk/Cargo.toml, otherwise pmd may fail. Leave this bug for now.

# Testing

Use `test-simplified-lxr` skill to test and verify LXR GC.

# Debugging

Refer to the `test-simplified-lxr` skill on how to run the benchmarks and verify the correctness of the simplified LXR GC.

To fix a crashing benchmark, you have the following options:
1. Use debug build (without `--release`) to get more debug info
2. Use GDB: add `--gdb --no-interactive` to the command, and it will automatically run the program in gdb, and print the backtrace if it crashes.
3. Inspect crash logs: hs_err_pid*.log

# PRECAUTIONS

* Don't commit, push, revert, or create/edit PRs or issues, unless the user explicitly ask you to do so.
* Do simplifications/refactorings one piece at a time. Don't aim to solve everything in one session.
* Benchmarks can run in parallel, but don't build jdk when other benchmarks or build task are still running.
* Do a `cargo fmt` under either `mmtk-core/` or `mmtk-openjdk/mmtk` before finish.

# Additional User Messages

$ARGUMENTS