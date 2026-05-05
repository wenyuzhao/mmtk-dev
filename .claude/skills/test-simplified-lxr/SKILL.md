---
name: test-simplified-lxr
description: Test simplified LXR GC under lxr-x/simplified branch
---

# Test simplified LXR GC

## Ensure the correct branches are checked out

* mmtk-core: `lxr-x/simplified` branch (based on tag `v0.32.0`)
* mmtk-openjdk: `lxr-x/jdk21-simplified` branch (based on tag `v0.32.0-jdk-21`)
* openjdk: `jdk-21.0.9+3-mmtk-lxr`

The above branches contain the simplified version of the LXR GC, which has removed some performance optimizations and other non-essential features to make it easier for upstreaming.

You can generate git diff for both mmtk-core and mmtk-openjdk to understand the changes in the two branches.

## Run tests

Please run the following command to test the correctness of the simplified LXR GC:

```bash
mmtk-jdk run --gc LXR -n 5 --heap 30M --bench xalan --build --no-weak-refs --no-class-unloading
```

Note that:
* Weak/soft/phantom/finalizable reference processing should be disabled with `--no-weak-refs`
* class unloading should be disable with `--no-class-unloading`
* The mmtk-jdk command sets `RUST_LOG=warning` by default if it is missing, to avoid verbose logging output.
* Testing one benchmark is not enough. You should try the following benchmark and heap size combinations:
    * lusearch:	40M
    * fop: 80M (without weak refs, 80M is the minimium heap size)
    * xalan: 30M
    * cassandra: 250M
    * pmd: 400M
* You only need to build once before running multiple benchmarks, if no code is edited between runs.
* Verify both debug builds and release builds (with `--release`)
* Always add `-n 5` to run for 5 iterations.
* Tests maybe flaky. Run it another time if it fails.
* Use gdb: add `--gdb --no-interactive` to the command, and it will automatically run the program in gdb, and print the backtrace if it crashes. This is useful for debugging.