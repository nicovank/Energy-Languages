ifndef PYTHON
PYTHON := python3
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
	sudo ../../../../scripts/RAPL/build/rapl --json "$(JSON)" ../../../../scripts/RAPL/build/time-limiter $(SECONDS) $(PYTHON) -OO regexredux.py 0 < ../../../../fasta-5000000.txt
