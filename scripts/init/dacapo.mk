init-dacapo: $(dacapo_dir)/dacapo-23.9-$(dacapo_chopin)-chopin

$(dacapo_dir)/dacapo-23.9-$(dacapo_chopin)-chopin:
	wget https://download.dacapobench.org/chopin/dacapo-23.9-$(dacapo_chopin)-chopin.zip
	unzip dacapo-23.9-$(dacapo_chopin)-chopin.zip
	sudo mkdir -p $(dacapo_dir)
	sudo rm -rf $(dacapo_dir)/dacapo-23.9-$(dacapo_chopin)-chopin
	sudo mv dacapo-23.9-$(dacapo_chopin)-chopin.jar $@.jar
	sudo mv dacapo-23.9-$(dacapo_chopin)-chopin $@
	rm dacapo-23.9-$(dacapo_chopin)-chopin.zip

$(dacapo_dir)/dacapo-evaluation-git-$(dacapo_commit).jar:
	wget https://github.com/wenyuzhao/lxr-pldi-2022-artifact/releases/download/_/dacapo-evaluation-git-$(dacapo_commit).jar
	sudo mkdir -p $(dacapo_dir)
	sudo mv dacapo-evaluation-git-$(dacapo_commit).jar $@

$(dacapo_dir)/dacapo-evaluation-git-$(dacapo_commit):
	rm -rf dacapo-evaluation-git-$(dacapo_commit)
	rm -f dacapo-evaluation-git-$(dacapo_commit).zip*
	wget https://github.com/wenyuzhao/lxr-pldi-2022-artifact/releases/download/_/dacapo-evaluation-git-$(dacapo_commit).zip.aa
	wget https://github.com/wenyuzhao/lxr-pldi-2022-artifact/releases/download/_/dacapo-evaluation-git-$(dacapo_commit).zip.ab
	wget https://github.com/wenyuzhao/lxr-pldi-2022-artifact/releases/download/_/dacapo-evaluation-git-$(dacapo_commit).zip.ac
	wget https://github.com/wenyuzhao/lxr-pldi-2022-artifact/releases/download/_/dacapo-evaluation-git-$(dacapo_commit).zip.ad
	cat dacapo-evaluation-git-$(dacapo_commit).zip.* > dacapo-evaluation-git-$(dacapo_commit).zip
	unzip dacapo-evaluation-git-$(dacapo_commit).zip
	sudo mkdir -p $(dacapo_dir)
	sudo rm -rf $(dacapo_dir)/dacapo-evaluation-git-$(dacapo_commit)
	sudo mv dacapo-evaluation-git-$(dacapo_commit) $@
	rm dacapo-evaluation-git-$(dacapo_commit).zip*

init-dacapo-9.12: $(dacapo_dir)/dacapo-9.12-bach.jar

$(dacapo_dir)/dacapo-9.12-bach.jar:
	wget https://github.com/wenyuzhao/lxr-pldi-2022-artifact/releases/download/_/dacapo-9.12-bach.jar
	sudo mkdir -p $(dacapo_dir)
	sudo rm -rf $@
	sudo mv dacapo-9.12-bach.jar $@
