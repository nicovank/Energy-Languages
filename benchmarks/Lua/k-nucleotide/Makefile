ifndef LUAC
LUAC := luac
endif

ifndef LUA
LUA := lua
endif

compile:
	$(LUAC) -o knucleotide.luac knucleotide.lua

run:
	$(LUA) knucleotide.luac 0 < ../../../fasta-25000000.txt

measure:
ifndef JSON
	$(error JSON is not defined)
endif
	sudo ../../../scripts/RAPL/build/rapl --json "$(JSON)" $(LUA) knucleotide.luac 0 < ../../../fasta-25000000.txt
