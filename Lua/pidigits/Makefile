ifndef LUAC
LUAC := luac
endif

ifndef LUA
LUA := lua
endif

compile:
	$(LUAC) -o pidigits.luac pidigits.lua

run:
	$(LUA) pidigits.luac 10000

measure:
ifndef JSON
	$(error JSON is not defined)
endif
	sudo ../../scripts/RAPL/build/rapl "$(JSON)" $(LUA) pidigits.luac 10000
