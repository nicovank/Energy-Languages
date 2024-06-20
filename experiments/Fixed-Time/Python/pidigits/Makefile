ifndef PYTHON
PYTHON := python3
endif

compile:
	$(PYTHON) -m compileall -o 2 pidigits.py

run:
	$(PYTHON) -OO pidigits.py 100000

measure:
ifndef JSON
	$(error JSON is not defined)
endif
	sudo ../../../scripts/RAPL/build/rapl --json "$(JSON)" $(PYTHON) -OO pidigits.py 100000
