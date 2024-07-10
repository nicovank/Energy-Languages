ifndef NODE
NODE := node
endif

compile:

run:
	$(NODE) fasta.js 2000000000

measure:
ifndef JSON
	$(error JSON is not defined)
endif
ifndef SECONDS
	$(error SECONDS is not defined)
endif
	sudo ../../../../scripts/RAPL/build/time-limiter $(SECONDS) ../../../../scripts/RAPL/build/rapl --json "$(JSON)" $(NODE) fasta.js 2000000000
