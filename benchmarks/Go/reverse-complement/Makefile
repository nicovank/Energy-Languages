ifndef GO
GO := go
endif

compile:
	$(GO) build -o revcomp_run revcomp.go

run:
	./revcomp_run 0 < ../../../fasta-25000000.txt

measure:
ifndef JSON
	$(error JSON is not defined)
endif
	sudo ../../../scripts/RAPL/build/rapl --json "$(JSON)" ./revcomp_run 0 < ../../../fasta-25000000.txt
