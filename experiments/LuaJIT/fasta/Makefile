ifndef LUAJIT
LUAJIT := luajit
endif

compile:

run:
	$(LUAJIT) fasta.lua 25000000

measure:
ifndef JSON
	$(error JSON is not defined)
endif
	sudo ../../../scripts/RAPL/build/rapl "$(JSON)" $(LUAJIT) fasta.lua 25000000
