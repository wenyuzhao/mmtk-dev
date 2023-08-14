PATH := ${mmtk_dev_dir}/depot_tools:${PATH}
PIN_V8_VERSION = 191b637f28c0e2c6ca5f2d6ac89377039a754337
v8_dir = ${mmtk_dev_dir}/v8

init-mmtk-jikesrvm:
	git submodule update --init --remote mmtk-jikesrvm
	cd mmtk-jikesrvm && git checkout master

init-jikesrvm:
	git submodule update --init --remote jikesrvm
	cd jikesrvm && git checkout master

init-jks-repos: init-mmtk-core init-mmtk-jikesrvm init-jikesrvm

build-jks:
	cd jikesrvm && ./bin/buildit localhost RBaseBaseSemiSpace --use-third-party-heap=../mmtk-jikesrvm --use-third-party-build-configs=../mmtk-jikesrvm/jikesrvm/build/configs/ --use-external-source=../mmtk-jikesrvm/jikesrvm/rvm/src --m32 --answer-yes

run-jks: 
	cd jikesrvm && LD_LIBRARY_PATH=dist/RBaseBaseSemiSpace_x86_64_m32-linux/ dist/RBaseBaseSemiSpace_x86_64_m32-linux/rvm -Xms75M -Xmx75M -jar /usr/share/benchmarks/dacapo/dacapo-9.12-bach.jar lusearch -n 5
