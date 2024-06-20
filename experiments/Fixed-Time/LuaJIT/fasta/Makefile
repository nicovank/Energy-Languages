ifndef LUAJIT
LUAJIT := luajit
endif

compile:
	$(LUAJIT) -b fasta.lua fasta.out

run:
	$(LUAJIT) fasta.out 2000000000

measure:
ifndef JSON
	$(error JSON is not defined)
endif
	sudo ../../../scripts/RAPL/build/rapl --json "$(JSON)" $(LUAJIT) fasta.out 2000000000
