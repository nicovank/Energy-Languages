ifndef TSC
TSC := tsc
endif

ifndef NODE
NODE := node
endif

compile:
	npm install
	$(TSC) --alwaysStrict -t ESNEXT mandelbrot.ts

run:
	$(NODE) mandelbrot.js 16000

measure:
ifndef JSON
	$(error JSON is not defined)
endif
ifndef SECONDS
	$(error SECONDS is not defined)
endif
	sudo ../../../../scripts/RAPL/build/rapl --json "$(JSON)" ../../../../scripts/RAPL/build/time-limiter $(SECONDS) $(NODE) mandelbrot.js 16000
