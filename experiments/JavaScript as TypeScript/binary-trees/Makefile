ifndef TSC
TSC := tsc
endif

ifndef NODE
NODE := node
endif

compile:
	npm install
	$(TSC) --skipLibCheck --alwaysStrict -t ESNEXT binarytrees.ts

run:
	$(NODE) binarytrees.js 21

measure:
ifndef JSON
	$(error JSON is not defined)
endif
	sudo ../../../scripts/RAPL/build/rapl --json "$(JSON)" $(NODE) binarytrees.js 21
