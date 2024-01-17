ifndef LUA
LUA := luajit
endif

compile:

run:
	$(LUA) regexredux.lua 0 < ../../../regexredux-input50000.txt

measure:
ifndef JSON
	$(error JSON is not defined)
endif
	sudo ../../../scripts/RAPL/build/rapl "$(JSON)" $(LUA) regexredux.lua 0 < ../../../regexredux-input50000.txt
