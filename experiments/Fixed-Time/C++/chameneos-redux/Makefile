-include ../Makefile.defaults

compile:
	$(CXX) $(CXXFLAGS) -pthread chameneosredux.cpp -o chameneosredux_run

run:
	./chameneosredux_run 500000000

measure:
ifndef JSON
	$(error JSON is not defined)
endif
ifndef SECONDS
	$(error SECONDS is not defined)
endif
	sudo ../../../../scripts/RAPL/build/time-limiter $(SECONDS) ../../../../scripts/RAPL/build/rapl --json "$(JSON)" ./chameneosredux_run 500000000
