ifndef PYTHON
PYTHON := pypy3
endif

compile:
	$(PYTHON) -m compileall -o 2 nbody.py

run:
	$(PYTHON) -OO nbody.py 1000000000

measure:
ifndef JSON
	$(error JSON is not defined)
endif
ifndef SECONDS
	$(error SECONDS is not defined)
endif
	sudo ../../../../scripts/RAPL/build/time-limiter $(SECONDS) ../../../../scripts/RAPL/build/rapl --json "$(JSON)" $(PYTHON) -OO nbody.py 1000000000
