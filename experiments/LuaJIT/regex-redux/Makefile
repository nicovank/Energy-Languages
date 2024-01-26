ifndef LUAJIT
LUAJIT := luajit
endif

compile:
	$(LUAJIT) -b regexredux.lua regexredux.out

run:
	$(LUAJIT) regexredux.out 0 < ../../../regexredux-input50000.txt

measure:
ifndef JSON
	$(error JSON is not defined)
endif
	sudo ../../../scripts/RAPL/build/rapl "$(JSON)" $(LUAJIT) regexredux.out 0 < ../../../regexredux-input50000.txt
