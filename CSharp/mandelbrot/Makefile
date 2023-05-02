compile:
	$(DOTNET) new console -o build -n build --force
	cp mandelbrot.csharpcore-5.csharpcore build/Program.cs
	$(DOTNET) build build/ -c Release --no-incremental

measure:
	sudo modprobe msr
	sudo ../../RAPL/main "$(DOTNET) run -c Release --project build/ --no-build -- 16000" CSharp mandelbrot

run:
	$(DOTNET) run -c Release --project build/ --no-build -- 16000

mem:
	/usr/bin/time -v $(DOTNET) run -c Release --project build/ --no-build -- 16000

valgrind:
	valgrind --tool=massif --stacks=yes $(DOTNET) run -c Release --project build/ --no-build -- 16000
