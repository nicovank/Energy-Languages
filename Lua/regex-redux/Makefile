ifndef LUAC
LUAC := luac
endif

ifndef LUA
LUA := lua
endif

compile:
	$(LUAC) -o regexredux.luac regexredux.lua

run:
	$(LUA) regexredux.luac 0 < ../../regexredux-input5000000.txt

measure:
ifndef JSON
	$(error JSON is not defined)
endif
	sudo ../../scripts/RAPL/build/rapl "$(JSON)" $(LUA) regexredux.luac 0 < ../../regexredux-input5000000.txt
