ifndef LUAJIT
LUAJIT := luajit
endif

compile:
	$(LUAJIT) -b knucleotide.lua knucleotide.out

run:
	$(LUAJIT) knucleotide.out 0 < ../../../../fasta-800000000.txt

measure:
ifndef JSON
	$(error JSON is not defined)
endif
ifndef SECONDS
	$(error SECONDS is not defined)
endif
	sudo ../../../../scripts/RAPL/build/rapl --json "$(JSON)" ../../../../scripts/RAPL/build/time-limiter $(SECONDS) $(LUAJIT) knucleotide.out 0 < ../../../../fasta-800000000.txt
