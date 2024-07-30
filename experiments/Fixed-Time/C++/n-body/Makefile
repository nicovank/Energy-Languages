-include ../Makefile.defaults

compile:
	$(CXX) $(CXXFLAGS) -fopenmp -mfpmath=sse -msse3 nbody.cpp -o nbody_run

run:
	./nbody_run 1000000000

measure:
ifndef JSON
	$(error JSON is not defined)
endif
ifndef SECONDS
	$(error SECONDS is not defined)
endif
	sudo ../../../../scripts/RAPL/build/rapl --json "$(JSON)" ../../../../scripts/RAPL/build/time-limiter $(SECONDS) ./nbody_run 1000000000
