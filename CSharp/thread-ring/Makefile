compile:
	$(DOTNET) new console -o build -n build --force
	cp threadring.csharpcore build/Program.cs
	$(DOTNET) build build/ -c Release --no-incremental

measure:
	sudo modprobe msr
	sudo ../../RAPL/main "$(DOTNET) run -c Release --project build/ --no-build -- 50000000"

run:
	$(DOTNET) run -c Release --project build/ --no-build -- 50000000