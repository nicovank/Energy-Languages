ifndef LUA
LUA := lua
endif

compile:

run:
	$(LUA) fannkuchredux.lua 12

measure:
ifndef JSON
	$(error JSON is not defined)
endif
	sudo ../../scripts/RAPL/build/rapl "$(JSON)" $(LUA) fannkuchredux.lua 12
