ifndef LUAJIT
LUAJIT := luajit
endif

compile:
	$(LUAJIT) -b spectralnorm.lua spectralnorm.out

run:
	$(LUAJIT) spectralnorm.out 150000

measure:
ifndef JSON
	$(error JSON is not defined)
endif
ifndef SECONDS
	$(error SECONDS is not defined)
endif
	sudo ../../../../scripts/RAPL/build/rapl --json "$(JSON)" ../../../../scripts/RAPL/build/time-limiter $(SECONDS) $(LUAJIT) spectralnorm.out 150000
