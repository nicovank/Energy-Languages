ifndef GO
GO := go
endif

compile:
	$(GO) build -o regexredux_run regexredux.go

run:
	./regexredux_run 0 < ../../../../fasta-5000000.txt

measure:
ifndef JSON
	$(error JSON is not defined)
endif
ifndef SECONDS
	$(error SECONDS is not defined)
endif
	sudo ../../../../scripts/RAPL/build/time-limiter $(SECONDS) ../../../../scripts/RAPL/build/rapl --json "$(JSON)" ./regexredux_run 0 < ../../../../fasta-5000000.txt
