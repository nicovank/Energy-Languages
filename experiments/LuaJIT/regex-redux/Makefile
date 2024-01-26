ifndef LUAJIT
LUAJIT := luajit
endif

compile:

run:
	$(LUAJIT) regexredux.lua 0 < ../../../regexredux-input50000.txt

measure:
ifndef JSON
	$(error JSON is not defined)
endif
	sudo ../../../scripts/RAPL/build/rapl "$(JSON)" $(LUAJIT) regexredux.lua 0 < ../../../regexredux-input50000.txt
