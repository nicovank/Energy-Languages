ifndef PYTHON
PYTHON := pypy3
endif

compile:
	$(PYTHON) -m compileall -o 2 spectralnorm.py

run:
	$(PYTHON) -OO spectralnorm.py 150000

measure:
ifndef JSON
	$(error JSON is not defined)
endif
	sudo ../../../scripts/RAPL/build/rapl --json "$(JSON)" $(PYTHON) -OO spectralnorm.py 150000
