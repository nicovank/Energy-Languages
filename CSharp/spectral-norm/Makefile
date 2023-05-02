compile:
	$(DOTNET) new console -o build -n build --force
	cp spectralnorm.csharpcore-3.csharpcore build/Program.cs
	$(DOTNET) build build/ -c Release --no-incremental

measure:
ifndef JSON
	$(error JSON is not defined)
endif
	sudo modprobe msr
	sudo ../../scripts/RAPL/build/rapl $(JSON) $(DOTNET) run -c Release --project build/ --no-build -- 5500

run:
	$(DOTNET) run -c Release --project build/ --no-build -- 5500

mem:
	/usr/bin/time -v  $(DOTNET) run -c Release --project build/ --no-build -- 5500

valgrind:
	valgrind --tool=massif --stacks=yes  $(DOTNET) run -c Release --project build/ --no-build -- 5500
