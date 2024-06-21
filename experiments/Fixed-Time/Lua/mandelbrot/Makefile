ifndef LUAC
LUAC := luac
endif

ifndef LUA
LUA := lua
endif

compile:
	$(LUAC) -o mandelbrot.luac mandelbrot.lua

run:
	$(LUA) mandelbrot.luac 16000

measure:
ifndef JSON
	$(error JSON is not defined)
endif
	sudo ../../../../scripts/RAPL/build/rapl --json "$(JSON)" $(LUA) mandelbrot.luac 16000
