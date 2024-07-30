ifndef PYTHON
PYTHON := python3
endif

compile:
	$(PYTHON) -m compileall -o 2 revcomp.py

run:
	$(PYTHON) -OO revcomp.py 0 < ../../../fasta-25000000.txt

measure:
ifndef JSON
	$(error JSON is not defined)
endif
	sudo ../../../scripts/RAPL/build/rapl --json "$(JSON)" $(PYTHON) -OO revcomp.py 0 < ../../../fasta-25000000.txt
