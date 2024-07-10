ifndef DOTNET
	DOTNET := dotnet
endif

compile:
	$(DOTNET) new console -o build -n build --force
	cp regexredux.cs build/Program.cs
	$(DOTNET) build build/ -c Release --no-incremental

run:
	$(DOTNET) run -c Release --project build/ --no-build -- 0 < ../../../../fasta-5000000.txt

measure:
ifndef JSON
	$(error JSON is not defined)
endif
ifndef SECONDS
	$(error SECONDS is not defined)
endif
	sudo ../../../../scripts/RAPL/build/time-limiter $(SECONDS) ../../../../scripts/RAPL/build/rapl --json "$(JSON)" $(DOTNET) run -c Release --project build/ --no-build -- 0 < ../../../../fasta-5000000.txt
