ifndef LUA
LUA := lua
endif

compile:

run:
	$(LUA) revcomp.lua 0 < ../../revcomp-input25000000.txt

measure:
ifndef JSON
	$(error JSON is not defined)
endif
	sudo ../../scripts/RAPL/build/rapl "$(JSON)" $(LUA) revcomp.lua 0 < ../../revcomp-input25000000.txt
