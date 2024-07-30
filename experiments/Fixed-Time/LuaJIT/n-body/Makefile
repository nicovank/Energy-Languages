ifndef LUAJIT
LUAJIT := luajit
endif

compile:
	$(LUAJIT) -b nbody.lua nbody.out

run:
	$(LUAJIT) nbody.out 1000000000

measure:
ifndef JSON
	$(error JSON is not defined)
endif
ifndef SECONDS
	$(error SECONDS is not defined)
endif
	sudo ../../../../scripts/RAPL/build/rapl --json "$(JSON)" ../../../../scripts/RAPL/build/time-limiter $(SECONDS) $(LUAJIT) nbody.out 1000000000
