mmtk-dev-env-version = 0.1.0

install:
	sudo apt update -y
	sudo apt install -y equivs
	equivs-build mmtk-dev-env.cfg
	sudo apt install -y --reinstall ./mmtk-dev-env_${mmtk-dev-env-version}_all.deb
