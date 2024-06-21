ifndef LUAJIT
LUAJIT := luajit
endif

compile:
	$(LUAJIT) -b fannkuchredux.lua fannkuchredux.out

run:
	$(LUAJIT) fannkuchredux.out 12

measure:
ifndef JSON
	$(error JSON is not defined)
endif
	sudo ../../../../scripts/RAPL/build/rapl --json "$(JSON)" $(LUAJIT) fannkuchredux.out 12
