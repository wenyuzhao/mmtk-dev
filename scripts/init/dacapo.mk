init-dacapo: $(dacapo_dir)/$(dacapo_chopin)

$(dacapo_dir)/$(dacapo_chopin):
	wget https://download.dacapobench.org/chopin/$(dacapo_chopin).zip
	unzip $(dacapo_chopin).zip
	sudo mkdir -p $(dacapo_dir)
	sudo rm -rf $(dacapo_dir)/$(dacapo_chopin)
	sudo mv $(dacapo_chopin).jar $@.jar
	sudo mv $(dacapo_chopin) $@
	rm $(dacapo_chopin).zip

init-dacapo-9.12: $(dacapo_dir)/dacapo-9.12-bach.jar

$(dacapo_dir)/dacapo-9.12-bach.jar:
	wget https://github.com/wenyuzhao/lxr-pldi-2022-artifact/releases/download/_/dacapo-9.12-bach.jar
	sudo mkdir -p $(dacapo_dir)
	sudo rm -rf $@
	sudo mv dacapo-9.12-bach.jar $@
