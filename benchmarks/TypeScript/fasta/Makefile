ifndef TSC
TSC := tsc
endif

ifndef NODE
NODE := node
endif

compile:
	npm install
	$(TSC) --skipLibCheck --alwaysStrict -t ESNEXT fasta.ts

run:
	$(NODE) fasta.js 25000000

measure:
ifndef JSON
	$(error JSON is not defined)
endif
	sudo ../../../scripts/RAPL/build/rapl --json "$(JSON)" $(NODE) fasta.js 25000000
