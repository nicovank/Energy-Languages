-include ../Makefile.defaults

compile:
	$(CC) $(CFLAGS) -pthread chameneosredux.c -o chameneosredux_run

run:
	./chameneosredux_run 500000000

measure:
ifndef JSON
	$(error JSON is not defined)
endif
ifndef SECONDS
	$(error SECONDS is not defined)
endif
	sudo ../../../../scripts/RAPL/build/rapl --json "$(JSON)" ../../../../scripts/RAPL/build/time-limiter $(SECONDS) ./chameneosredux_run 500000000
