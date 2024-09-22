ifndef TSC
TSC := tsc
endif

ifndef NODE
NODE := node
endif

compile:
	npm install
	$(TSC) --skipLibCheck --alwaysStrict -t ESNEXT fannkuchredux.ts

run:
	$(NODE) fannkuchredux.js 12

measure:
ifndef JSON
	$(error JSON is not defined)
endif
	sudo ../../../scripts/RAPL/build/rapl --json "$(JSON)" $(NODE) fannkuchredux.js 12
