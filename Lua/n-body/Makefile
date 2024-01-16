ifndef LUA
LUA := lua
endif

compile:

run:
	$(LUA) nbody.lua 50000000

measure:
ifndef JSON
	$(error JSON is not defined)
endif
	sudo ../../scripts/RAPL/build/rapl "$(JSON)" $(LUA) nbody.lua 50000000
