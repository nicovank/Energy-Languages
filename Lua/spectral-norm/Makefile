ifndef LUA
LUA := lua
endif

compile:

run:
	$(LUA) spectralnorm.lua 5500

measure:
ifndef JSON
	$(error JSON is not defined)
endif
	sudo ../../scripts/RAPL/build/rapl "$(JSON)" $(LUA) spectralnorm.lua 5500
