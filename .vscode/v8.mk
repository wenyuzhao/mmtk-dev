
export RUST_BACKTRACE=1
export RUSTFLAGS=-Awarnings
# export MMTK_PLAN=$(gc)
# export RUSTUP_TOOLCHAIN=nightly-2020-07-08
export RUSTUP_TOOLCHAIN=nightly-2020-12-20
export RUST_LOG=info
export gm=./tools/dev/gm.py

setup:
	fetch v8
	mkdir -p v8/out/x64.debug-mmtk
	cp .vscode/args.gn ./v8/out/x64.debug-mmtk/args.gn
	cd mmtk-v8/mmtk && eval `ssh-agent` && ssh-add

build:
	cd mmtk-v8/mmtk && cargo build --features nogc
	cd v8 && $(gm) x64.debug-mmtk

test: build
	cd v8 && python2 tools/run-tests.py -p ci --outdir=out/x64.debug-mmtk benchmarks/*
	cd v8 && python2 tools/run-tests.py -p ci --outdir=out/x64.debug-mmtk mjsunit/regress/*
	cd v8 && python2 tools/run-tests.py -p ci --outdir=out/x64.debug-mmtk unittests/*