ifndef NODE
NODE := node
endif

compile:

run:
	$(NODE) regexredux.js 0 < ../../../../fasta-5000000.txt

measure:
ifndef JSON
	$(error JSON is not defined)
endif
	sudo ../../../../scripts/RAPL/build/rapl --json "$(JSON)" $(NODE) regexredux.js 0 < ../../../../fasta-5000000.txt
