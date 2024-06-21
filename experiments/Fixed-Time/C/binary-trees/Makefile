-include ../Makefile.defaults

compile:
	$(CC) $(CFLAGS) $(shell pkg-config --cflags apr-1) -fopenmp binarytrees.c -o binarytrees_run $(shell pkg-config --libs apr-1)

run:
	./binarytrees_run 27

measure:
ifndef JSON
	$(error JSON is not defined)
endif
	sudo ../../../../scripts/RAPL/build/rapl --json "$(JSON)" ./binarytrees_run 27
