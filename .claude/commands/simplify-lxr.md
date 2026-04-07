# Simplify LXR GC for upstreaming

`lxr-x/simplfied` branch in mmtk-core and `lxr-x/jdk21-simplfied` branch in mmtk-openjdk contain the implementation of the LXR garbage collector.

`lxr-x/simplfied` in mmtk-core is based on tag `v0.32.0`
`lxr-x/jdk21-simplfied` in mmtk-openjdk is based on tag `v0.32.0-jdk-21`

Both branches contains:
* The core LXR GC algorithm
* Additional performance optimizations
* Changes to the MMTk interface and other components of MMTk
* Changes to support additional fetures, e.g. weak refs and class unloading
* Custom instrumentation and logging code
* Changes to the other GCs in MMTk
* Other stale dead code

You need to work on the `lxr-x/simplfied` and `lxr-x/jdk21-simplfied`.

You need to simplify the two branches so that the user can easily upstream a simplified version of LXR GC easily, although the performance may not be as good as the original one.

Assume the upstream is at `v0.32.0` and `v0.32.0-jdk-21`.

# Compare and understand git diff

Generate git diff for both mmtk-core and mmtk-openjdk, and understand the changes in the two branches.

# Start a small refactoring/simplification task

The diff may be over 8K LOC, You can't do all the changes in one go.
Only pick a few components/aspects of the codebase that can be simplified/refactored, and perform this task.

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

# Testing

After making changes, Please run the following command to test the correctness of the simplified LXR GC:

```bash
mmtk-jdk run --gc LXR -n 5 --heap 30M --bench xalan --build --no-weak-refs
```

Note that:
1. Weak/soft/phantom/finalizable reference processing should be disabled with `--no-weak-refs`
2. The mmtk-jdk command sets `RUST_LOG=warning` by default if it is missing, to avoid verbose logging output.
3. Testing one benchmark is not enough. You should try the following benchmark and heap size combinations:
    * lusearch:	40M
    * fop: 30M
    * xalan: 30M
    * cassandra: 250M
    * pmd: 400M
4. You only need to build once before running multiple benchmarks, if no code is edited between runs.
4. Also verify with release builds with `--release`

# PRECAUTIONS

* Don't commit, push, revert, or create/edit PRs or issues, unless the user explicitly ask you to do so.
* Do simplifications/refactorings one piece at a time. Don't aim to solve everything in one session.