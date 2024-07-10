ifndef PYTHON
PYTHON := pypy3
endif

compile:
	$(PYTHON) -m compileall -o 2 regexredux.py

run:
	$(PYTHON) -OO regexredux.py 0 < ../../../../fasta-5000000.txt

measure:
ifndef JSON
	$(error JSON is not defined)
endif
ifndef SECONDS
	$(error SECONDS is not defined)
endif
	sudo ../../../../scripts/RAPL/build/time-limiter $(SECONDS) ../../../../scripts/RAPL/build/rapl --json "$(JSON)" $(PYTHON) -OO regexredux.py 0 < ../../../../fasta-5000000.txt
