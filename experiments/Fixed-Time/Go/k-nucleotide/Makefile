ifndef GO
GO := go
endif

compile:
	$(GO) build -o knucleotide_run knucleotide.go

run:
	./knucleotide_run 0 < ../../../../fasta-800000000.txt

measure:
ifndef JSON
	$(error JSON is not defined)
endif
ifndef SECONDS
	$(error SECONDS is not defined)
endif
	sudo ../../../../scripts/RAPL/build/rapl --json "$(JSON)" ../../../../scripts/RAPL/build/time-limiter $(SECONDS) ./knucleotide_run 0 < ../../../../fasta-800000000.txt
