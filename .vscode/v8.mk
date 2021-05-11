gc=Page

export MMTK_PLAN=$(gc)
export MMTK_THREADS=1
export RUST_BACKTRACE=1
export RUSTFLAGS=-Awarnings
export RUST_LOG=info
export gm=./tools/dev/gm.py

profile=optdebug-mmtk
# gc=plan

setup:
	fetch v8
	mkdir -p v8/out/x64.$(profile)
	cp .vscode/args.gn ./v8/out/x64.$(profile)/args.gn

mmtk:
	cd mmtk-v8/mmtk && cargo build

build: mmtk
	cd v8 && $(gm) x64.$(profile).all

test: build
	cd v8 && $(gm) x64.$(profile).checkall --exit-after-n-failures=0

!: mmtk
	cd v8 && ./_debug.py out/x64.debug-mmtk/d8 --test test/mjsunit/mjsunit.js test/mjsunit/regress/regress-4271.js --random-seed=-864837579 --nohard-abort --enable-slow-asserts --verify-heap --testing-d8-test-runner

snapshot:
	cd v8 && gdb --args out/x64.$(profile)/mksnapshot --turbo_instruction_scheduling --target_os=linux --target_arch=x64 --embedded_src out/x64.$(profile)/gen/embedded.S --embedded_variant Default --random-seed 314159265 --startup_blob out/x64.$(profile)/snapshot_blob.bin --native-code-counters --no-turbo-rewrite-far-jumps --no-turbo-verify-allocation --verify-heap