ifndef NODE
NODE := node
endif

compile:
ifndef NNNNN
	$(error NNNNN is not defined)
endif
	sed s/NNNNN/$(NNNNN)/ fannkuchredux.js.in > fannkuchredux.js

run:
	$(NODE) fannkuchredux.js 12

measure:
ifndef JSON
	$(error JSON is not defined)
endif
	sudo ../../../scripts/RAPL/build/rapl --json "$(JSON)" $(NODE) fannkuchredux.js 12
