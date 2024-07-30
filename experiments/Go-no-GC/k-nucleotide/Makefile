ifndef GO
GO := go
endif

compile:
	$(GO) build -o knucleotide_run knucleotide.go

run:
	env GOGC=off ./knucleotide_run 0 < ../../../fasta-25000000.txt

measure:
ifndef JSON
	$(error JSON is not defined)
endif
	sudo ../../../scripts/RAPL/build/rapl --json "$(JSON)" env GOGC=off ./knucleotide_run 0 < ../../../fasta-25000000.txt
