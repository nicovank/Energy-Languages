compile:
	$(DOTNET) new console -o build -n build --force
	cp fannkuchredux.csharpcore-4.csharpcore build/Program.cs
	$(DOTNET) build build/ -c Release --no-incremental

measure:
	sudo modprobe msr
	sudo ../../RAPL/main "$(DOTNET) run -c Release --project build/ --no-build -- 12" CSharp fannkuch-redux

run:
	$(DOTNET) run -c Release --project build/ --no-build -- 12

mem:
	/usr/bin/time -v  $(DOTNET) run -c Release --project build/ --no-build -- 12

valgrind:
	valgrind --tool=massif --stacks=yes  $(DOTNET) run -c Release --project build/ --no-build -- 12
