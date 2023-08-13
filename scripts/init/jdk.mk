init-mmtk-openjdk:
	git submodule update --init --remote mmtk-openjdk
	cd mmtk-openjdk && git checkout master
ifeq ($(lxr),1)
	cd mmtk-openjdk && (git remote -v | grep -w wenyu || (git remote add wenyu https://github.com/wenyuzhao/mmtk-openjdk.git && git fetch wenyu))
	cd mmtk-openjdk && git checkout lxr
endif

init-openjdk:
	git submodule update --init --remote openjdk
	cd openjdk && git checkout jdk-11.0.19+1-mmtk
ifeq ($(lxr),1)
	cd openjdk && git checkout jdk-11.0.19+1-mmtk-lxr
endif

init-jdk-repos: init-mmtk-core init-mmtk-openjdk init-openjdk