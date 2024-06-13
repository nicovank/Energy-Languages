ifndef LUAC
LUAC := luac
endif

ifndef LUA
LUA := lua
endif

compile:
	$(LUAC) -o binarytrees.luac binarytrees.lua

run:
	$(LUA) binarytrees.luac 21

measure:
ifndef JSON
	$(error JSON is not defined)
endif
	sudo ../../scripts/RAPL/build/rapl --json "$(JSON)" $(LUA) binarytrees.luac 21
