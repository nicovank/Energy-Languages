ifndef LUAJIT
LUAJIT := luajit
endif

compile:

run:
	$(LUAJIT) mandelbrot.lua 16000

measure:
ifndef JSON
	$(error JSON is not defined)
endif
	sudo ../../../scripts/RAPL/build/rapl "$(JSON)" $(LUAJIT) mandelbrot.lua 16000
