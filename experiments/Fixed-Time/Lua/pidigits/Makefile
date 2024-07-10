ifndef LUAC
LUAC := luac
endif

ifndef LUA
LUA := lua
endif

compile:
	$(LUAC) -o pidigits.luac pidigits.lua

run:
	$(LUA) pidigits.luac 100000

measure:
ifndef JSON
	$(error JSON is not defined)
endif
ifndef SECONDS
	$(error SECONDS is not defined)
endif
	sudo ../../../../scripts/RAPL/build/rapl --json "$(JSON)" ../../../../scripts/RAPL/build/time-limiter $(SECONDS) $(LUA) pidigits.luac 100000
