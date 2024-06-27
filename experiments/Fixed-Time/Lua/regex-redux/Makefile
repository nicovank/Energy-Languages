ifndef LUAC
LUAC := luac
endif

ifndef LUA
LUA := lua
endif

compile:
	$(LUAC) -o regexredux.luac regexredux.lua

run:
	$(LUA) regexredux.luac 0 < ../../../../fasta-5000000.txt

measure:
ifndef JSON
	$(error JSON is not defined)
endif
	sudo ../../../../scripts/RAPL/build/rapl --json "$(JSON)" $(LUA) regexredux.luac 0 < ../../../../fasta-5000000.txt
