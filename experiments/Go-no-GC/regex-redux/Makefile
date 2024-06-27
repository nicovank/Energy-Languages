ifndef GO
GO := go
endif

compile:
	$(GO) build -o regexredux_run regexredux.go

run:
	env GOGC=off ./regexredux_run 0 < ../../../fasta-5000000.txt

measure:
ifndef JSON
	$(error JSON is not defined)
endif
	sudo ../../../scripts/RAPL/build/rapl --json "$(JSON)" env GOGC=off ./regexredux_run 0 < ../../../fasta-5000000.txt
