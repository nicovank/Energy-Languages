ifndef LUAJIT
LUAJIT := luajit
endif

compile:
	$(LUAJIT) -b revcomp.lua revcomp.out

run:
	$(LUAJIT) revcomp.out 0 < ../../../../fasta-25000000.txt

measure:
ifndef JSON
	$(error JSON is not defined)
endif
	sudo ../../../../scripts/RAPL/build/rapl --json "$(JSON)" $(LUAJIT) revcomp.out 0 < ../../../../fasta-25000000.txt
