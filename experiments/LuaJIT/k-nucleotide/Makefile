ifndef LUAJIT
LUAJIT := luajit
endif

compile:

run:
	$(LUAJIT) knucleotide.lua 0 < ../../../knucleotide-input25000000.txt

measure:
ifndef JSON
	$(error JSON is not defined)
endif
	sudo ../../../scripts/RAPL/build/rapl "$(JSON)" $(LUAJIT) knucleotide.lua 0 < ../../../knucleotide-input25000000.txt
