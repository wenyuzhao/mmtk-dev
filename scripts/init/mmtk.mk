init-mmtk-core:
	git submodule update --init --remote mmtk-core
	cd mmtk-core && git checkout master
ifeq ($(lxr),1)
	cd mmtk-core && (git remote -v | grep -w wenyu || (git remote add wenyu https://github.com/wenyuzhao/mmtk-core.git && git fetch wenyu))
	cd mmtk-core && git checkout lxr
endif