-include ../Makefile.defaults

compile:
	$(CC) $(CFLAGS) -fopenmp fannkuchredux.c -o fannkuchredux_run

run:
	./fannkuchredux_run 12

measure:
ifndef JSON
	$(error JSON is not defined)
endif
ifndef SECONDS
	$(error SECONDS is not defined)
endif
	sudo ../../../../scripts/RAPL/build/time-limiter $(SECONDS) ../../../../scripts/RAPL/build/rapl --json "$(JSON)" ./fannkuchredux_run 12
