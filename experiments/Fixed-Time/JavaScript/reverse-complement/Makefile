ifndef NODE
NODE := node
endif

compile:

run:
	$(NODE) revcomp.js 0 < ../../../../fasta-25000000.txt

measure:
ifndef JSON
	$(error JSON is not defined)
endif
ifndef SECONDS
	$(error SECONDS is not defined)
endif
	sudo ../../../../scripts/RAPL/build/time-limiter $(SECONDS) ../../../../scripts/RAPL/build/rapl --json "$(JSON)" $(NODE) revcomp.js 0 < ../../../../fasta-25000000.txt
