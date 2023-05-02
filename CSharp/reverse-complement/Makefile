compile:
	$(DOTNET) new console -o build -n build --force
	cp revcomp.csharpcore-2.csharpcore build/Program.cs
	$(DOTNET) build build/ -c Release --no-incremental

measure:
ifndef JSON
	$(error JSON is not defined)
endif
	sudo modprobe msr
	sudo ../../scripts/RAPL/build/rapl $(JSON) $(DOTNET) run -c Release --project build/ --no-build -- 0 < ../../revcomp-input25000000.txt

run:
	$(DOTNET) run -c Release --project build/ --no-build -- 0 < ../../revcomp-input25000000.txt

mem:
	/usr/bin/time -v  $(DOTNET) run -c Release --project build/ --no-build -- 0 < ../../revcomp-input25000000.txt

valgrind:
	valgrind --tool=massif --stacks=yes   $(DOTNET) run -c Release --project build/ --no-build -- 0 < ../../revcomp-input25000000.txt
