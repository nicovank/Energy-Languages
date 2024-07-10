ifndef NODE
NODE := node
endif

compile:

run:
	$(NODE) knucleotide.js 0 < ../../../../fasta-800000000.txt

measure:
ifndef JSON
	$(error JSON is not defined)
endif
ifndef SECONDS
	$(error SECONDS is not defined)
endif
	sudo ../../../../scripts/RAPL/build/rapl --json "$(JSON)" ../../../../scripts/RAPL/build/time-limiter $(SECONDS) $(NODE) knucleotide.js 0 < ../../../../fasta-800000000.txt
