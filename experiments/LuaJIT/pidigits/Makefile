ifndef LUAJIT
LUAJIT := luajit
endif

compile:
	$(LUAJIT) -b pidigits.lua pidigits.out

run:
	$(LUAJIT) pidigits.out 10000

measure:
ifndef JSON
	$(error JSON is not defined)
endif
	sudo ../../../scripts/RAPL/build/rapl "$(JSON)" $(LUAJIT) pidigits.out 10000
