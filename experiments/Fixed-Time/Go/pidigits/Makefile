ifndef GO
GO := go
endif

compile:
	$(GO) build -o pidigits_run pidigits.go

run:
	./pidigits_run 100000

measure:
ifndef JSON
	$(error JSON is not defined)
endif
ifndef SECONDS
	$(error SECONDS is not defined)
endif
	sudo ../../../../scripts/RAPL/build/time-limiter $(SECONDS) ../../../../scripts/RAPL/build/rapl --json "$(JSON)" ./pidigits_run 100000
