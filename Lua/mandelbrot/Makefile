ifndef LUA
LUA := lua
endif

compile:

run:
	$(LUA) mandelbrot.lua 16000

measure:
ifndef JSON
	$(error JSON is not defined)
endif
	sudo ../../scripts/RAPL/build/rapl "$(JSON)" $(LUA) mandelbrot.lua 16000
