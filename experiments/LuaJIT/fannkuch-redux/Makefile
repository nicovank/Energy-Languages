ifndef LUAJIT
LUAJIT := luajit
endif

compile:

run:
	$(LUAJIT) fannkuchredux.lua 12

measure:
ifndef JSON
	$(error JSON is not defined)
endif
	sudo ../../../scripts/RAPL/build/rapl "$(JSON)" $(LUAJIT) fannkuchredux.lua 12
