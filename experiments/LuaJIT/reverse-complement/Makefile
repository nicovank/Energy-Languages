ifndef LUAC
LUAC := luac
endif

ifndef LUA
LUA := lua
endif

compile:
	$(LUAC) -o revcomp.luac revcomp.lua

run:
	$(LUA) revcomp.luac 0 < ../../../revcomp-input25000000.txt

measure:
ifndef JSON
	$(error JSON is not defined)
endif
	sudo ../../../scripts/RAPL/build/rapl "$(JSON)" $(LUA) revcomp.luac 0 < ../../../revcomp-input25000000.txt
