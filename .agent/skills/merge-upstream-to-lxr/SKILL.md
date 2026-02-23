---
name: merge-upstream-to-lxr
description: Instructions to Merge Upstream Changes to LXR GC
---

# Merge Upstream Changes to LXR GC

Follow the following steps to merge the newer base branches from origin into the `lxr-merge` branch of both mmtk-core and mmtk-openjdk repos.

## 1. Preparation

The user should provide you with the target base branches/tags/commit-hashes for both repos. For example: `v0.31.0`

You need to work on the `lxr-merge` branches of both repos:

```console
$ cd mmtk-core && git checkout lxr-merge && cd ..
$ cd mmtk-openjdk && git checkout lxr-merge && cd ..
```

## 2. Initiate merge

```console
$ cd mmtk-core && git merge <target_base_branch> && cd ..
$ cd mmtk-openjdk && git merge <target_base_branch> && cd ..
```

## 3. Resolve all conflicts

Please carefully review each conflict and the origonal intention of the change in both LXR and upstream repos. Then, resolve the conflict in a way that (1) keeps LXR working (2) make LXR's code compliant with the upstream design changes.

The LXR commit history:
    * https://github.com/mmtk/mmtk-core/commits/lxr-merge
    * https://github.com/mmtk/mmtk-openjdk/commits/lxr-merge

The upstream commit history:
    * https://github.com/mmtk/mmtk-core/commits/master
    * https://github.com/mmtk/mmtk-openjdk/commits/jdk-11


## 4. Verify

### Build

Ensure the project and the repos can build correctly. Fix any errors.

Since mmtk-core does not depend on other local repos, you can verify this one first:
    * `cd mmtk-core && cargo build` (or cargo check)

After ensuring mmtk-core is correct, verify mmtk-openjdk:
    * `cd mmtk-openjdk/mmtk && cargo build` (or cargo check)

Finally the whole project: `uv run mmtk-jdk build`

### Run benchmarks

After openjdk can build, run the following command on four different benchmarks (but only use LXR GC):

`uv run mmtk-jdk run --gc=LXR --bench=lusearch --heap=500M -n 5`

Available benchmarks and heap sizes:
* `lusearch`: 500M
* `h2`: 1200M
* `tomcat`: 200M
* `fop`: 100M
