# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

mmtk-dev is a development workspace for MMTk (Memory Management Toolkit) — a framework for building garbage collectors in Rust. It contains the MMTk core library, VM bindings (OpenJDK, V8, JikesRVM), benchmarking infrastructure, and helper scripts.

Key subdirectories are git submodules:
- `mmtk-core/` — Core GC framework (Rust library, edition 2021, MSRV 1.84, pinned Rust 1.92.0)
- `mmtk-openjdk/` — OpenJDK VM binding for MMTk
- `openjdk/` — Patched OpenJDK source with third-party heap support

## Build & Run Commands

### Building and Running OpenJDK with MMTk
The primary CLI tool is `mmtk-jdk` (installed via `uv`):
```bash
# Build + run (fastdebug, exploded image)
# Note that tradebeans and tradesoap do not work with exploded images
uv run mmtk-jdk r --gc Immix --bench lusearch --heap 500M --exploded --build

# Release build + run
uv run mmtk-jdk r --gc LXR --bench xalan --heap 30M --build --release

# Build only
uv run mmtk-jdk build --release

# Run without rebuilding
uv run mmtk-jdk r --gc LXR --bench lusearch --heap 40M

# Shorthand: 'r' = run, 'b' = build, -x = --exploded, -r = --release
```

Key flags: `--gc <GC>`, `--bench <benchmark>`, `--heap <size>`, `--build`, `--release`, `--exploded`, `--no-weak-refs`, `--features <comma_separated_cargo_features>`, `-n <iterations>`

### Building mmtk-core Rust code directly
```bash
cd mmtk-core
cargo build           # Debug build
cargo build --release # Release build
cargo test            # Run unit tests
cargo test --features mock_test  # Run mock VM tests
```

### Running benchmarks for testing
Common benchmark/heap combinations for correctness testing:
- `lusearch` at `40M`
- `fop` at `30M`
- `xalan` at `30M`
- `cassandra` at `250M`
- `pmd` at `400M`

## Architecture

### MMTk-Core (`mmtk-core/src/`)
- `plan/` — GC algorithm implementations (NoGC, SemiSpace, MarkSweep, Immix, GenImmix, StickyImmix, MarkCompact, PageProtect, Compressor, LXR). Each plan defines its collection strategy, mutator configuration, and work packets.
- `policy/` — Memory space policies (Immortal, LargeObject, MallocSpace, etc.) — the building blocks plans compose.
- `scheduler/` — Work packet scheduler for parallel/concurrent GC phases.
- `vm/` — VM binding trait interface. VMs implement these traits to integrate with MMTk.
- `util/` — Allocators, heap management, metadata (side/header), copy semantics, statistics.
- `memory_manager.rs` — Public API surface that VM bindings call into.
- `mmtk.rs` — Core `MMTK` struct holding all GC state.

### MMTk-OpenJDK Binding (`mmtk-openjdk/mmtk/src/`)
- `api.rs` — C FFI entry points called from OpenJDK's C++ code.
- `object_model.rs` / `object_scanning.rs` — OpenJDK object layout and traversal.

### Python Tooling (`scripts/mmtk_dev/`)
- `jdk/` — `mmtk-jdk` CLI: build, run, benchmark OpenJDK with MMTk.
- `jks/` — `mmtk-jks` CLI for JikesRVM. (stale)
- Entry points defined in `pyproject.toml`. Managed with `uv`.

## Active Development: LXR GC

The LXR garbage collector sits in the following key branches:
* Fully-featured LXR GC:
    - `lxr` in mmtk-core (based on `v0.32.0`)
    - `lxr-x/jdk21` in mmtk-openjdk (based on `v0.32.0-jdk-21`)
* A simplified version of LXR GC:
    - `lxr-x/simplfied` in mmtk-core (based on `v0.32.0`)
    - `lxr-x/jdk21-simplfied` in mmtk-openjdk (based on `v0.32.0-jdk-21`)

## Notes

- `RUST_LOG=warning` is set by default by `mmtk-jdk` when not already set.
- The Cargo workspace uses LTO for release builds.
- Clippy allows `upper_case_acronyms` and `uninlined_format_args`.
- Evaluation/benchmarking infrastructure lives in `evaluation/` with YAML configs; results are run on remote machines (e.g., `boar.moma`).
