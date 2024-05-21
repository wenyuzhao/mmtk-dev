
lxr=0
dacapo_chopin=dacapo-23.11-chopin
dacapo_dir=/usr/share/benchmarks/dacapo
mmtk_dev_dir:=$(shell dirname $(realpath $(firstword $(MAKEFILE_LIST))))

init-jdk: | python-packages init-dacapo init-jdk-repos probes

init-jdk-docker: | init-dacapo init-jdk-repos probes
	docker compose --profile jdk build

init-v8: | python-packages init-v8-repos

init-v8-docker: | init-v8-repos
	docker compose --profile v8 build

init-jks-docker: | init-dacapo-9.12 init-jks-repos
	docker compose --profile jks build

python-packages:
	pipx install running-ng
	pipx install poetry
	poetry install

install-debian-packages:
	cd scripts/init/debs && make install

include scripts/init/mmtk.mk
include scripts/init/jdk.mk
include scripts/init/v8.mk
include scripts/init/jks.mk
include scripts/init/dacapo.mk
include scripts/init/probes.mk
