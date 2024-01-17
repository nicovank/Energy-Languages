ifndef LUA
LUA := luajit
endif

compile:

run:
	$(LUA) binarytrees.lua 21

measure:
ifndef JSON
	$(error JSON is not defined)
endif
	sudo ../../../scripts/RAPL/build/rapl "$(JSON)" $(LUA) binarytrees.lua 21
