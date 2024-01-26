ifndef LUAJIT
LUAJIT := luajit
endif

compile:
	$(LUAJIT) -b nbody.lua nbody.out

run:
	$(LUAJIT) nbody.out 50000000

measure:
ifndef JSON
	$(error JSON is not defined)
endif
	sudo ../../../scripts/RAPL/build/rapl "$(JSON)" $(LUAJIT) nbody.out 50000000
