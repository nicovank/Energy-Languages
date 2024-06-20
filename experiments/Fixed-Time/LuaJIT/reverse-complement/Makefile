ifndef LUAJIT
LUAJIT := luajit
endif

compile:
	$(LUAJIT) -b revcomp.lua revcomp.out

run:
	$(LUAJIT) revcomp.out 0 < ../../../revcomp-input25000000.txt

measure:
ifndef JSON
	$(error JSON is not defined)
endif
	sudo ../../../scripts/RAPL/build/rapl --json "$(JSON)" $(LUAJIT) revcomp.out 0 < ../../../revcomp-input25000000.txt
