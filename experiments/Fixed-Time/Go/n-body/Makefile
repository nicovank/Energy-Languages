ifndef GO
GO := go
endif

compile:
	$(GO) build -o nbody_run nbody.go

run:
	./nbody_run 1000000000

measure:
ifndef JSON
	$(error JSON is not defined)
endif
ifndef SECONDS
	$(error SECONDS is not defined)
endif
	sudo ../../../../scripts/RAPL/build/time-limiter $(SECONDS) ../../../../scripts/RAPL/build/rapl --json "$(JSON)" ./nbody_run 1000000000
