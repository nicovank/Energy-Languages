-include ../Makefile.defaults

compile:
	$(CXX) $(CXXFLAGS) -fopenmp regexredux.cpp -o regexredux_run -lboost_regex

run:
	./regexredux_run 0 < ../../../../fasta-5000000.txt

measure:
ifndef JSON
	$(error JSON is not defined)
endif
ifndef SECONDS
	$(error SECONDS is not defined)
endif
	sudo ../../../../scripts/RAPL/build/rapl --json "$(JSON)" ../../../../scripts/RAPL/build/time-limiter $(SECONDS) ./regexredux_run 0 < ../../../../fasta-5000000.txt
