ifndef LUA
LUA := lua
endif

compile:

run:
	$(LUA) fasta.lua 25000000

measure:
ifndef JSON
	$(error JSON is not defined)
endif
	sudo ../../scripts/RAPL/build/rapl "$(JSON)" $(LUA) fasta.lua 25000000
