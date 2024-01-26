ifndef LUAJIT
LUAJIT := luajit
endif

compile:

run:
	$(LUAJIT) spectralnorm.lua 5500

measure:
ifndef JSON
	$(error JSON is not defined)
endif
	sudo ../../../scripts/RAPL/build/rapl "$(JSON)" $(LUAJIT) spectralnorm.lua 5500
