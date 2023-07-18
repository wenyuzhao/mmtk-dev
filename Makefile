
lxr=0
dacapo=04132797
dacapo_dir=/usr/share/benchmarks/dacapo

init-jdk: debian-packages python-packages init-mmtk-core init-mmtk-openjdk init-openjdk init-dacapo

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

init-dacapo: $(dacapo_dir)/dacapo-evaluation-git-$(dacapo).jar $(dacapo_dir)/dacapo-evaluation-git-$(dacapo).zip

$(dacapo_dir)/dacapo-evaluation-git-$(dacapo).jar:
	wget https://github.com/wenyuzhao/lxr-pldi-2022-artifact/releases/download/_/dacapo-evaluation-git-$(dacapo).jar
	sudo mkdir -p $(dacapo_dir)
	sudo mv dacapo-evaluation-git-$(dacapo).jar $@

$(dacapo_dir)/dacapo-evaluation-git-$(dacapo).zip:
	rm dacapo-evaluation-git-$(dacapo).zip*
	wget https://github.com/wenyuzhao/lxr-pldi-2022-artifact/releases/download/_/dacapo-evaluation-git-$(dacapo).zip.aa
	wget https://github.com/wenyuzhao/lxr-pldi-2022-artifact/releases/download/_/dacapo-evaluation-git-$(dacapo).zip.ab
	wget https://github.com/wenyuzhao/lxr-pldi-2022-artifact/releases/download/_/dacapo-evaluation-git-$(dacapo).zip.ac
	wget https://github.com/wenyuzhao/lxr-pldi-2022-artifact/releases/download/_/dacapo-evaluation-git-$(dacapo).zip.ad
	sudo mkdir -p $(dacapo_dir)
	cat dacapo-evaluation-git-$(dacapo).zip.* > dacapo-evaluation-git-$(dacapo).zip
	sudo mv dacapo-evaluation-git-$(dacapo).zip $@
	rm dacapo-evaluation-git-$(dacapo).zip*

python-packages:
	poetry install --no-root
	pipx install running-ng

debian-packages:
	sudo apt-get update -y
	sudo apt-get install -y python3-full python3-pip pipx default-jdk openjdk-11-jdk build-essential git autoconf libfontconfig1-dev dos2unix build-essential libx11-dev libxext-dev libxrender-dev libxtst-dev libxt-dev libcups2-dev libasound2-dev libxrandr-dev
