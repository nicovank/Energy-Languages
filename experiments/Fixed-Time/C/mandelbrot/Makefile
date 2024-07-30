-include ../Makefile.defaults

compile:
	$(CC) $(CFLAGS) -std=gnu89 -mno-fma -fno-finite-math-only -mfpmath=sse -msse2 -fopenmp mandelbrot.c -o mandelbrot_run

run:
	./mandelbrot_run 16000

measure:
ifndef JSON
	$(error JSON is not defined)
endif
ifndef SECONDS
	$(error SECONDS is not defined)
endif
	sudo ../../../../scripts/RAPL/build/rapl --json "$(JSON)" ../../../../scripts/RAPL/build/time-limiter $(SECONDS) ./mandelbrot_run 16000
