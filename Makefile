
lxr=0

init-jdk: python-packages init-mmtk-core init-mmtk-openjdk init-openjdk init-dacapo

init-mmtk-core: mmtk-core/Cargo.toml
	git submodule update --init --remote mmtk-core
	cd mmtk-core && git checkout master
ifeq ($(lxr),1)
	cd mmtk-core && git remote add wenyu https://github.com/wenyuzhao/mmtk-core.git && git fetch wenyu && git checkout -b lxr wenyu/lxr
endif

init-mmtk-openjdk: mmtk-openjdk/README.md
	git submodule update --init --remote mmtk-openjdk
	cd mmtk-core && git checkout master
ifeq ($(lxr),1)
	cd mmtk-openjdk && git remote add wenyu https://github.com/wenyuzhao/mmtk-openjdk.git && git fetch wenyu && git checkout -b lxr wenyu/lxr
endif

init-openjdk: openjdk/LICENSE
	git submodule update --init --remote openjdk
	cd mmtk-core && git checkout jdk-11.0.19+1-mmtk
ifeq ($(lxr),1)
	cd openjdk && git checkout jdk-11.0.19+1-mmtk-lxr
endif

init-dacapo: /usr/share/benchmarks/dacapo/dacapo-evaluation-git-04132797.jar
# 	git submodule update --init --remote openjdk
# 	cd mmtk-core && git checkout jdk-11.0.19+1-mmtk
# ifeq ($(lxr),1)
# 	cd mmtk-core && git checkout jdk-11.0.19+1-mmtk-lxr
# endif

python-packages:
	poetry install --no-root