# Verify LXR GC

Verify the correctness of the LXR GC in current active branches, by running the following command with a few different benchmarks:

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

# Bug Fix

Try fix any crashes or bugs discovered during verification.

# PRECAUTIONS

* Benchmarks can run in parallel, but don't build jdk when other benchmarks or build task are still running.
* Don't commit, push, revert, or create/edit PRs or issues, unless the user explicitly ask you to do so.
