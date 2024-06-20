ifndef NODE
NODE := node
endif

compile:

run:
	$(NODE) binarytrees.js 27

measure:
ifndef JSON
	$(error JSON is not defined)
endif
	sudo ../../../scripts/RAPL/build/rapl --json "$(JSON)" $(NODE) binarytrees.js 27
