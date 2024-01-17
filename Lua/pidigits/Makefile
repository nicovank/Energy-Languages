ifndef LUA
LUA := lua
endif

compile:

run:
	$(LUA) pidigits.lua 10000

measure:
ifndef JSON
	$(error JSON is not defined)
endif
	sudo ../../scripts/RAPL/build/rapl "$(JSON)" $(LUA) pidigits.lua 10000
