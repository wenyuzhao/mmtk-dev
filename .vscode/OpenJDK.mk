vm_root = ./mmtk-openjdk/repos/openjdk
conf=linux-x86_64-normal-server-$(profile)
vm_args:=-XX:MetaspaceSize=1G

# Interpreter only
# common_args=-server -XX:+DisableExplicitGC -Xint
# Int+C1 only
# common_args=-server -XX:+DisableExplicitGC -XX:TieredStopAtLevel=1
# Int+C2 only
vm_args:=$(vm_args) -server -XX:+DisableExplicitGC -XX:-TieredCompilation
# Int+C1+C2
# common_args=-server -XX:+DisableExplicitGC

vm-config:
	@echo "🟦 Config: $(conf) (mmtk-plan=$(gc))"
	@cd mmtk-openjdk/mmtk && eval `ssh-agent` && ssh-add
	@cd $(vm_root) && sh configure --disable-warnings-as-errors --with-debug-level=$(profile) --with-target-bits=64 --disable-zip-debug-info

vm-build:
	@echo "🟦 Building: $(conf) (mmtk-plan=$(gc))"
	@cd $(vm_root) && make --no-print-directory CONF=$(conf) THIRD_PARTY_HEAP=$$PWD/../../openjdk

vm-run: java=$(vm_root)/build/$(conf)/jdk/bin/java
vm-run:
	$(java) $(vm_args) $(heap_args) $(mmtk_args) $(bm_args)

vm-clean:
	@cd $(vm_root) && make clean CONF=$(CONF) --no-print-directory
