-include ../Makefile.defaults

compile:
	$(CC) $(CFLAGS) -mfpmath=sse -msse3 -fopenmp fasta.c -o fasta_run

run:
	./fasta_run 2000000000

measure:
ifndef JSON
	$(error JSON is not defined)
endif
ifndef SECONDS
	$(error SECONDS is not defined)
endif
	sudo ../../../../scripts/RAPL/build/rapl --json "$(JSON)" ../../../../scripts/RAPL/build/time-limiter $(SECONDS) ./fasta_run 2000000000
