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

init-dacapo-9.12: $(dacapo_dir)/dacapo-9.12-bach.jar

$(dacapo_dir)/dacapo-9.12-bach.jar:
	wget https://github.com/wenyuzhao/lxr-pldi-2022-artifact/releases/download/_/dacapo-9.12-bach.jar
	sudo mkdir -p $(dacapo_dir)
	sudo rm -rf $@
	sudo mv dacapo-9.12-bach.jar $@
