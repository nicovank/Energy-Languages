ifndef LUAJIT
LUAJIT := luajit
endif

compile:
	$(LUAJIT) -b knucleotide.lua knucleotide.out

run:
	$(LUAJIT) knucleotide.out 0 < ../../../knucleotide-input25000000.txt

measure:
ifndef JSON
	$(error JSON is not defined)
endif
	sudo ../../../scripts/RAPL/build/rapl "$(JSON)" $(LUAJIT) knucleotide.out 0 < ../../../knucleotide-input25000000.txt
