ifndef LUAJIT
LUAJIT := luajit
endif

compile:
	$(LUAJIT) -b mandelbrot.lua mandelbrot.out

run:
	$(LUAJIT) mandelbrot.out 16000

measure:
ifndef JSON
	$(error JSON is not defined)
endif
ifndef SECONDS
	$(error SECONDS is not defined)
endif
	sudo ../../../../scripts/RAPL/build/time-limiter $(SECONDS) ../../../../scripts/RAPL/build/rapl --json "$(JSON)" $(LUAJIT) mandelbrot.out 16000
