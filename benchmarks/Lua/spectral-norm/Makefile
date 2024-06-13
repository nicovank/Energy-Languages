ifndef LUAC
LUAC := luac
endif

ifndef LUA
LUA := lua
endif

compile:
	$(LUAC) -o spectralnorm.luac spectralnorm.lua

run:
	$(LUA) spectralnorm.luac 5500

measure:
ifndef JSON
	$(error JSON is not defined)
endif
	sudo ../../scripts/RAPL/build/rapl --json "$(JSON)" $(LUA) spectralnorm.luac 5500
