ifndef TSC
TSC := tsc
endif

ifndef NODE
NODE := node
endif

compile:
	npm install
	$(TSC) --skipLibCheck --alwaysStrict -t ESNEXT mandelbrot.ts

run:
	$(NODE) mandelbrot.js 16000

measure:
ifndef JSON
	$(error JSON is not defined)
endif
	sudo ../../../scripts/RAPL/build/rapl --json "$(JSON)" $(NODE) mandelbrot.js 16000
