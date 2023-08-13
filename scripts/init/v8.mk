PATH := ${mmtk_dev_dir}/depot_tools:${PATH}
PIN_V8_VERSION = 191b637f28c0e2c6ca5f2d6ac89377039a754337
v8_dir = ${mmtk_dev_dir}/v8

init-mmtk-v8:
	git submodule update --init --remote mmtk-v8
	cd mmtk-v8 && git checkout master

init-depot-tools:
	[ -f ${mmtk_dev_dir}/depot_tools/README.md ] || git clone https://chromium.googlesource.com/chromium/tools/depot_tools.git

init-v8: init-depot-tools
	gclient
	[ -f ${v8_dir}/README.md ] || (fetch v8 && git -C v8 checkout ${PIN_V8_VERSION})
	gclient sync
	[ -f ${v8_dir}/out/x64.optdebug-mmtk/args.gn ] || (mkdir -p ${v8_dir}/out/x64.optdebug-mmtk && cp ${mmtk_dev_dir}/scripts/v8-args/args-optdebug.gn ${v8_dir}/out/x64.optdebug-mmtk/args.gn)

init-v8-repos: init-mmtk-core init-mmtk-v8 init-depot-tools init-v8

build-v8:
	cd mmtk-v8/mmtk && cargo build --features nogc
	PATH=${mmtk_dev_dir}/depot_tools:${PATH} cd v8 && ./tools/dev/gm.py x64.optdebug-mmtk

check-v8:
	cd mmtk-v8/mmtk && cargo build --features nogc
	PATH=${mmtk_dev_dir}/depot_tools:${PATH} cd v8 && ./tools/dev/gm.py x64.optdebug-mmtk.checkall