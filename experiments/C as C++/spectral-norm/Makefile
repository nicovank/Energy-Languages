-include ../Makefile.defaults

compile:
	$(CC) $(CFLAGS) -std=c++98 -fopenmp -mfpmath=sse -msse2 spectralnorm.c -o spectralnorm_run -lm

run:
	./spectralnorm_run 5500

measure:
ifndef JSON
	$(error JSON is not defined)
endif
	sudo ../../../scripts/RAPL/build/rapl --json "$(JSON)" ./spectralnorm_run 5500
