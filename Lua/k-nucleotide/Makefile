ifndef LUA
LUA := lua
endif

compile:

run:
	$(LUA) knucleotide.lua 0 < ../../knucleotide-input25000000.txt

measure:
ifndef JSON
	$(error JSON is not defined)
endif
	sudo ../../scripts/RAPL/build/rapl "$(JSON)" $(LUA) knucleotide.lua 0 < ../../knucleotide-input25000000.txt
