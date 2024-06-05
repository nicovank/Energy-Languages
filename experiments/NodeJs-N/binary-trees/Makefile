ifndef NODE
NODE := node
endif

compile:
ifndef NNNNN
	$(error NNNNN is not defined)
endif
	sed s/NNNNN/$(NNNNN)/ binarytrees.java.in > binarytrees.java

run:
	$(NODE) binarytrees.js 21

measure:
ifndef JSON
	$(error JSON is not defined)
endif
	sudo ../../scripts/RAPL/build/rapl --json "$(JSON)" $(NODE) binarytrees.js 21
