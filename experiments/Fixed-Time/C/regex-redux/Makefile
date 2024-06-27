-include ../Makefile.defaults

compile:
	$(CC) $(CFLAGS) -fopenmp regexredux.c -o regexredux_run -lpcre

run:
	./regexredux_run 0 < ../../../../fasta-5000000.txt

measure:
ifndef JSON
	$(error JSON is not defined)
endif
	sudo ../../../../scripts/RAPL/build/rapl --json "$(JSON)" ./regexredux_run 0 < ../../../../fasta-5000000.txt
