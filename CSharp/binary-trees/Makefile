compile:
	$(DOTNET) new console -o build -n build --force
	cp binarytrees.csharpcore-4.csharpcore build/Program.cs
	$(DOTNET) build build/ -c Release --no-incremental

measure:
	sudo modprobe msr
	sudo ../../RAPL/main "$(DOTNET) run -c Release --project build/ --no-build -- 21" CSharp binary-trees

run:
	$(DOTNET) run -c Release --project build/ --no-build -- 21

mem:
	/usr/bin/time -v $(DOTNET) run -c Release --project build/ --no-build -- 21

valgrind:
	valgrind --tool=massif --stacks=yes $(DOTNET) run -c Release --project build/ --no-build -- 21
