ifndef LUAC
LUAC := luac
endif

ifndef LUA
LUA := lua
endif

compile:
	$(LUAC) -o fannkuchredux.luac fannkuchredux.lua

run:
	$(LUA) fannkuchredux.luac 12

measure:
ifndef JSON
	$(error JSON is not defined)
endif
	sudo ../../../scripts/RAPL/build/rapl "$(JSON)" $(LUA) fannkuchredux.luac 12
