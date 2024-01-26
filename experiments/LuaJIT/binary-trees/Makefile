ifndef LUAJIT
LUAJIT := luajit
endif

compile:

run:
	$(LUAJIT) binarytrees.lua 21

measure:
ifndef JSON
	$(error JSON is not defined)
endif
	sudo ../../../scripts/RAPL/build/rapl "$(JSON)" $(LUAJIT) binarytrees.lua 21
