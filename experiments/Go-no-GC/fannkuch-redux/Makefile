ifndef GO
GO := go
endif

compile:
	$(GO) build -o fannkuchredux_run fannkuchredux.go

run:
	env GOGC=off ./fannkuchredux_run 12

measure:
ifndef JSON
	$(error JSON is not defined)
endif
	sudo ../../../scripts/RAPL/build/rapl --json "$(JSON)" env GOGC=off ./fannkuchredux_run 12
