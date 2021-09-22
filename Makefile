vm?=jdk
# vm?=v8
# vm?=jikes

include ./.vscode/$(vm).mk

config-probe:
	@cd evaluation/probes && make all


ci-tests:
	@cd mmtk-core && bash ./.github/scripts/ci-build.sh
	@cd mmtk-core && bash ./.github/scripts/ci-test.sh
	@cd mmtk-core && bash ./.github/scripts/ci-style.sh

bench-rsync: moma=shrew
bench-rsync:
	# @rsync -azR --info=progress2 --exclude ~/./MMTk-Dev/evaluation/configs --exclude ~/./MMTk-Dev/evaluation/scratch --exclude ~/./MMTk-Dev/evaluation/results --exclude ~/./MMTk-Dev/evaluation/tmp ~/./MMTk-Dev/evaluation $(moma).moma:/home/wenyuz/
	rsync -azR --info=progress2 ~/./MMTk-Dev/running-ng $(moma).moma:/home/wenyuz/
	rsync -azR --info=progress2 ~/./MMTk-Dev/evaluation/configs/$(config) $(moma).moma:/home/wenyuz/
	rsync -azR --info=progress2 ~/./MMTk-Dev/evaluation/configs/*.yml $(moma).moma:/home/wenyuz/
	rsync -azR --info=progress2 ~/./MMTk-Dev/evaluation/advice $(moma).moma:/home/wenyuz/
	rsync -azR --info=progress2 ~/./MMTk-Dev/evaluation/probes $(moma).moma:/home/wenyuz/
	# bin/runbms 8 1 &> runbms.log
	# running runbms ./evaluation/results/log ./evaluation/configs/flb/flb.yml 8 -i 20 --skip-oom 1 --skip-timeout 1
# running runbms ./evaluation/results/log ./evaluation/configs/flb-rc/config.yml 8 3 5 -i 20 --skip-oom 1 --skip-timeout 1 > x.log