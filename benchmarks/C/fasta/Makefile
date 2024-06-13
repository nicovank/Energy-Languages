-include ../Makefile.defaults

compile:
	$(CC) $(CFLAGS) -mfpmath=sse -msse3 -fopenmp fasta.c -o fasta_run

run:
	./fasta_run 25000000

measure:
ifndef JSON
	$(error JSON is not defined)
endif
	sudo ../../scripts/RAPL/build/rapl --json "$(JSON)" ./fasta_run 25000000
