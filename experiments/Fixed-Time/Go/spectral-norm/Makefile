ifndef GO
GO := go
endif

compile:
	$(GO) build -o spectralnorm_run spectralnorm.go

run:
	./spectralnorm_run 150000

measure:
ifndef JSON
	$(error JSON is not defined)
endif
ifndef SECONDS
	$(error SECONDS is not defined)
endif
	sudo ../../../../scripts/RAPL/build/rapl --json "$(JSON)" ../../../../scripts/RAPL/build/time-limiter $(SECONDS) ./spectralnorm_run 150000
