ifndef LUAJIT
LUAJIT := luajit
endif

compile:
	$(LUAJIT) -b regexredux.lua regexredux.out

run:
	$(LUAJIT) regexredux.out 0 < ../../../../fasta-5000000.txt

measure:
ifndef JSON
	$(error JSON is not defined)
endif
ifndef SECONDS
	$(error SECONDS is not defined)
endif
	sudo ../../../../scripts/RAPL/build/rapl --json "$(JSON)" ../../../../scripts/RAPL/build/time-limiter $(SECONDS) $(LUAJIT) regexredux.out 0 < ../../../../fasta-5000000.txt
