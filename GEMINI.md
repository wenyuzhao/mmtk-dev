# Project Structure

This project contains the MMTk with OpenJDK support.

MMTk is a language-neutral Garbage Collection (GC) framework.
It supports multiple language runtimes, but we only care about OpenJDK 11 here.

It has three main sub-repos (as git submodules):
    * `mmtk-core/`: The MMTk Core
    * `mmtk-openjdk/`: The MMTk Binding for OpenJDK
    * `openjdk/`: The OpenJDK 11 repo with MMTk support.

## MMTk-Core

The mmtk-core repo can point to two remote repos:
    * The master branch: https://github.com/mmtk/mmtk-core
    * For most other branches, they sits in my fork: https://github.com/wenyuzhao/mmtk-core
        * For example, the LXR GC is at https://github.com/wenyuzhao/mmtk-core/tree/lxr

### Garbage Collectors (Plans)

MMTk supports multiple garbage collectors, they all sit under *mmtk-core/src/plan/*.

For example, Immix GC is at *mmtk-core/src/plan/immix/*, it contains the following files:
    * *barrier.rs* -- Barriers used by Immix. They are just for experiments as Immix needs no barriers.
    * *gc_work.rs* -- Declares some work packet types for Immix GC
    * *global.rs* -- handles some global steps/events
    * *mutator.rs* -- Defines the mutator struct.

### Work Packets

MMTk uses work packets to schedule GC tasks across multiple GC worker threads.
Please refer to https://www.steveblackburn.org/pubs/papers/packet-oopsla-2025.pdf for more details. Note that this repo only implements the **P** variant discussed in the paper, and some details may not match precisely with the paper.

*mmtk-core/src/scheduler/* contains most of the work packet implementations and the scheduler implementation.
    * *gc_work.rs* -- Work packets
    * *scheduler.rs* -- The scheduler
    * *work_bucket.rs* -- Work buckets
    * *worker.rs* -- Worker threads

### Policies

MMTk has multiple policies (i.e. heap memory spaces). They sit under *mmtk-core/src/policy/*.
For example, Both Immix and LXR uses two spaces: ImmixSpace (*mmtk-core/src/policy/immix*) and LargeObjectSpace (*mmtk-core/src/policy/largeobjectspace.rs*)

For Immix space, please refer to the following two papers for the memory layout and allocation policy:
    * https://www.steveblackburn.org/pubs/papers/immix-pldi-2008.pdf
    * https://www.steveblackburn.org/pubs/papers/lxr-pldi-2022.pdf

### Allocators

Each MMTk policy requires a matching allocator. Allocators sit under *mmtk-core/src/util/alloc/*.
For example, Immix uses ImmixSpace as the main space, and the ImmixAllocator as the default allocator (this is declated at *mmtk-core/src/plan/immix/mutator.rs*).

## MMTk-OpenJDK

MMTk-OpenJDK is a binding between MMTk Core and OpenJDK. It sits under *mmtk-openjdk/*.

The mmtk-openjdk repo can point to two remote repos:
    * The main branch (the branch name is jdk-11): https://github.com/mmtk/mmtk-openjdk
    * For most other branches, they sits in my fork: https://github.com/wenyuzhao/mmtk-openjdk
        * For example, the LXR GC is at https://github.com/wenyuzhao/mmtk-openjdk/tree/lxr


`mmtk-openjdk/mmtk` contains the Rust part of the binding.
`mmtk-openjdk/openjdk` contains the C++ part of the binding.

## OpenJDK

`openjdk/` contains the my fork of the openjdk11 repo.

# How to build and run benchmarks

**To build OpenJDK with MMTk**:

`uv run mmtk-jdk build [--clean]`

**To run benchmarks**:

`uv run mmtk-jdk run --gc=<gc-name> --bench=<benchmark-name> --heap=<heap-size> -n 5 [--build]`

for example: `uv run mmtk-jdk run --gc=LXR --bench=lusearch --heap=500M -n 5`

Available GCs:
* `Immix`
* `LXR`

Available benchmarks and heap sizes:
* `lusearch`: 500M
* `h2`: 1200M
* `tomcat`: 200M
* `fop`: 100M

**To run benchmarks with gdb for debugging**:

`uv run mmtk-jdk run --gc=LXR --bench=lusearch --heap=500M -n 5 --gdb`

This will give you an interactive GDB session. The program is paused at start, type `r` to start running the program. Type `quit` to exit gdb when you finish.

# LXR GC

The `lxr` or `lxr-merge` branch of both `mmtk-core` and `mmtk-openjdk` repos contains the LXR GC implementation.

Please refer to the following papers for LXR design details:
    * https://www.steveblackburn.org/pubs/papers/lxr-pldi-2022.pdf
    * https://www.steveblackburn.org/pubs/papers/prod-oopsla-2025.pdf

Please note that the latest LXR may differ from the paper. Always refer to the code for the latest implementation details.

The source code is also available at https://github.com/wenyuzhao/mmtk-core/tree/lxr

# IMPORTANT: NEVER FINALIZE/COMMIT MERGE AUTOMATICALLY!