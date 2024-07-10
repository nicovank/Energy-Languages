-include ../Makefile.defaults

compile:
	$(CC) $(CFLAGS) -fopenmp revcomp.c -o revcomp_run

run:
	./revcomp_run 0 < ../../../../fasta-25000000.txt

measure:
ifndef JSON
	$(error JSON is not defined)
endif
ifndef SECONDS
	$(error SECONDS is not defined)
endif
	sudo ../../../../scripts/RAPL/build/time-limiter $(SECONDS) ../../../../scripts/RAPL/build/rapl --json "$(JSON)" ./revcomp_run 0 < ../../../../fasta-25000000.txt
