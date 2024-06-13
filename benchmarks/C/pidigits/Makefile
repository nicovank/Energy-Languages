-include ../Makefile.defaults

compile:
	$(CC) $(CFLAGS) pidigits.c -o pidigits_run -lgmp

run:
	./pidigits_run 10000

measure:
ifndef JSON
	$(error JSON is not defined)
endif
	sudo ../../scripts/RAPL/build/rapl --json "$(JSON)" ./pidigits_run 10000
