ifndef PYTHON
PYTHON := python3
endif

compile:
	$(PYTHON) -m compileall -o 2 binarytrees.py

run:
	$(PYTHON) -OO binarytrees.py 27

measure:
ifndef JSON
	$(error JSON is not defined)
endif
ifndef SECONDS
	$(error SECONDS is not defined)
endif
	sudo ../../../../scripts/RAPL/build/rapl --json "$(JSON)" ../../../../scripts/RAPL/build/time-limiter $(SECONDS) $(PYTHON) -OO binarytrees.py 27
