---
name: about-simplified-lxr
description: Useful information about the simplified LXR GC implementation in mmtk-core and mmtk-openjdk.
---

# Simplified LXR GC

`lxr-x/simplified` branch in mmtk-core and `lxr-x/jdk21-simplified` branch in mmtk-openjdk contain the implementation of the LXR garbage collector.

`lxr-x/simplified` in mmtk-core is based on tag `v0.32.0`
`lxr-x/jdk21-simplified` in mmtk-openjdk is based on tag `v0.32.0-jdk-21`

The two branches are forked from the original LXR GC implementation. Both branches contains the core LXR GC algorithm without additional optimizations and features.

Note: The simplification process is still ongoing, and the branches may not be fully simplified yet. You can refer to the commit history and the current progress section for more details on what has been simplified so far.

The purpose of the simplification is to make easier to upstream, although the performance may not be as good as the original one.

Assume the upstream is at `v0.32.0` and `v0.32.0-jdk-21`.

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