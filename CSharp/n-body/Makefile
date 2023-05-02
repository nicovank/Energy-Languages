compile:
	$(DOTNET) new console -o build -n build --force
	cp nbody.csharpcore-3.csharpcore build/Program.cs
	$(DOTNET) build build/ -c Release --no-incremental

measure:
	sudo modprobe msr
	sudo ../../RAPL/main "$(DOTNET) run -c Release --project build/ --no-build -- 50000000" CSharp n-body

run:
	$(DOTNET) run -c Release --project build/ --no-build -- 50000000

mem:
	/usr/bin/time -v  $(DOTNET) run -c Release --project build/ --no-build -- 50000000

valgrind:
	valgrind --tool=massif --stacks=yes  $(DOTNET) run -c Release --project build/ --no-build -- 50000000
