
lxr=0
dacapo=04132797
dacapo_dir=/usr/share/benchmarks/dacapo

init-jdk: python-packages init-jdk-repos init-dacapo probes

init-jdk-repos: init-mmtk-core init-mmtk-openjdk init-openjdk probes

init-jdk-docker: init-jdk-repos
	docker compose build

init-mmtk-core:
	git submodule update --init --remote mmtk-core
	cd mmtk-core && git checkout master
ifeq ($(lxr),1)
	cd mmtk-core && (git remote -v | grep -w wenyu || (git remote add wenyu https://github.com/wenyuzhao/mmtk-core.git && git fetch wenyu))
	cd mmtk-core && git checkout lxr
endif

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

init-dacapo: $(dacapo_dir)/dacapo-evaluation-git-$(dacapo).jar $(dacapo_dir)/dacapo-evaluation-git-$(dacapo)

$(dacapo_dir)/dacapo-evaluation-git-$(dacapo).jar:
	wget https://github.com/wenyuzhao/lxr-pldi-2022-artifact/releases/download/_/dacapo-evaluation-git-$(dacapo).jar
	sudo mkdir -p $(dacapo_dir)
	sudo mv dacapo-evaluation-git-$(dacapo).jar $@

$(dacapo_dir)/dacapo-evaluation-git-$(dacapo):
	rm -rf dacapo-evaluation-git-$(dacapo)
	rm -f dacapo-evaluation-git-$(dacapo).zip*
	wget https://github.com/wenyuzhao/lxr-pldi-2022-artifact/releases/download/_/dacapo-evaluation-git-$(dacapo).zip.aa
	wget https://github.com/wenyuzhao/lxr-pldi-2022-artifact/releases/download/_/dacapo-evaluation-git-$(dacapo).zip.ab
	wget https://github.com/wenyuzhao/lxr-pldi-2022-artifact/releases/download/_/dacapo-evaluation-git-$(dacapo).zip.ac
	wget https://github.com/wenyuzhao/lxr-pldi-2022-artifact/releases/download/_/dacapo-evaluation-git-$(dacapo).zip.ad
	cat dacapo-evaluation-git-$(dacapo).zip.* > dacapo-evaluation-git-$(dacapo).zip
	unzip dacapo-evaluation-git-$(dacapo).zip
	sudo mkdir -p $(dacapo_dir)
	sudo rm -rf $(dacapo_dir)/dacapo-evaluation-git-$(dacapo)
	sudo mv dacapo-evaluation-git-$(dacapo) $@
	rm dacapo-evaluation-git-$(dacapo).zip*

probes: evaluation/probes/librust_mmtk_probe.so evaluation/probes/librust_mmtk_probe_32.so evaluation/probes/probes-java6.jar evaluation/probes/probes.jar evaluation/probes/libperf_statistics.so

evaluation/probes/libperf_statistics.so:
	mkdir -p evaluation/probes
	cd evaluation/probes && wget https://github.com/wenyuzhao/lxr-pldi-2022-artifact/releases/download/_/$(@F)

evaluation/probes/%:
	mkdir -p evaluation/probes
	cd evaluation/probes && wget https://github.com/anupli/probes/releases/download/20230127-snapshot/$(@F)

python-packages:
	pipx install running-ng
	pipx install poetry
	poetry install --no-root

install-debian-packages:
	cd scripts/debs && make install
