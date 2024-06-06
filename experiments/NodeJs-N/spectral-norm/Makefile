ifndef NODE
NODE := node
endif

compile:
ifndef NNNNN
	$(error NNNNN is not defined)
endif
	sed s/NNNNN/$(NNNNN)/ spectralnorm.js.in > spectralnorm.js

run:
	$(NODE) spectralnorm.js 5500

measure:
ifndef JSON
	$(error JSON is not defined)
endif
	sudo ../../../scripts/RAPL/build/rapl --json "$(JSON)" $(NODE) spectralnorm.js 5500
