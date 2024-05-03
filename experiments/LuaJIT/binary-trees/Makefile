ifndef LUAJIT
LUAJIT := luajit
endif

compile:
	$(LUAJIT) -b binarytrees.lua binarytrees.out

run:
	$(LUAJIT) binarytrees.out 21

measure:
ifndef JSON
	$(error JSON is not defined)
endif
	sudo ../../../scripts/RAPL/build/rapl --json "$(JSON)" $(LUAJIT) binarytrees.out 21
