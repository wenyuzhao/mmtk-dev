# TASK := JikesRVM
# TASK := JikesRVM.local
TASK := OpenJDK

include $(TASK).mk

# Build probes
probes:
	@rsync -av ./running/ $(RUN_MACHINE):$(REMOTE_HOME)/running
	$(SSH) "cd $(REMOTE_HOME)/running/probes && make probes.jar OPTION=-m32"

# VSCode Settings:
#
# "[makefile]": {
#   "editor.detectIndentation": false,
#   "editor.insertSpaces": false,
#   "editor.tabSize": 4
#   "editor.renderWhitespace": "boundary",
# }