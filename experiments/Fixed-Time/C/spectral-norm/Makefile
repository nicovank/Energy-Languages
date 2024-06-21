-include ../Makefile.defaults

compile:
	$(CC) $(CFLAGS) -fopenmp -mfpmath=sse -msse2 spectralnorm.c -o spectralnorm_run -lm

run:
	./spectralnorm_run 150000

measure:
ifndef JSON
	$(error JSON is not defined)
endif
	sudo ../../../../scripts/RAPL/build/rapl --json "$(JSON)" ./spectralnorm_run 150000
