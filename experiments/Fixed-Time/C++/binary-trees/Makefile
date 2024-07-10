-include ../Makefile.defaults

compile:
	$(CXX) $(CXXFLAGS) $(shell pkg-config --cflags apr-1) -fopenmp binarytrees.cpp -o binarytrees_run $(shell pkg-config --libs apr-1)

run:
	./binarytrees_run 27

measure:
ifndef JSON
	$(error JSON is not defined)
endif
ifndef SECONDS
	$(error SECONDS is not defined)
endif
	sudo ../../../../scripts/RAPL/build/rapl --json "$(JSON)" ../../../../scripts/RAPL/build/time-limiter $(SECONDS) ./binarytrees_run 27
