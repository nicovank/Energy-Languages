ifndef LUAJIT
LUAJIT := luajit
endif

compile:
	$(LUAJIT) -b pidigits.lua pidigits.out

run:
	$(LUAJIT) pidigits.out 100000

measure:
ifndef JSON
	$(error JSON is not defined)
endif
ifndef SECONDS
	$(error SECONDS is not defined)
endif
	sudo ../../../../scripts/RAPL/build/time-limiter $(SECONDS) ../../../../scripts/RAPL/build/rapl --json "$(JSON)" $(LUAJIT) pidigits.out 100000
