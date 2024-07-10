ifndef LUAJIT
LUAJIT := luajit
endif

compile:
	$(LUAJIT) -b binarytrees.lua binarytrees.out

run:
	$(LUAJIT) binarytrees.out 27

measure:
ifndef JSON
	$(error JSON is not defined)
endif
ifndef SECONDS
	$(error SECONDS is not defined)
endif
	sudo ../../../../scripts/RAPL/build/time-limiter $(SECONDS) ../../../../scripts/RAPL/build/rapl --json "$(JSON)" $(LUAJIT) binarytrees.out 27
