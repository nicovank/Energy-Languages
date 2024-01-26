ifndef LUAJIT
LUAJIT := luajit
endif

compile:

run:
	$(LUAJIT) revcomp.lua 0 < ../../../revcomp-input25000000.txt

measure:
ifndef JSON
	$(error JSON is not defined)
endif
	sudo ../../../scripts/RAPL/build/rapl "$(JSON)" $(LUAJIT) revcomp.lua 0 < ../../../revcomp-input25000000.txt
