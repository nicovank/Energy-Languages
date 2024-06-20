ifndef NODE
NODE := node
endif

compile:

run:
	$(NODE) spectralnorm.js 150000

measure:
ifndef JSON
	$(error JSON is not defined)
endif
	sudo ../../../scripts/RAPL/build/rapl --json "$(JSON)" $(NODE) spectralnorm.js 150000
