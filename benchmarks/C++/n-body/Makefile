-include ../Makefile.defaults

compile:
	$(CXX) $(CXXFLAGS) -fopenmp -mfpmath=sse -msse3 nbody.cpp -o nbody_run

run:
	./nbody_run 50000000

measure:
ifndef JSON
	$(error JSON is not defined)
endif
	sudo ../../../scripts/RAPL/build/rapl --json "$(JSON)" ./nbody_run 50000000
