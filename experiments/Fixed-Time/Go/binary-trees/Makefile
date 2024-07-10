ifndef GO
GO := go
endif

compile:
	$(GO) build -o binarytrees_run binarytrees.go

run:
	./binarytrees_run 27

measure:
ifndef JSON
	$(error JSON is not defined)
endif
ifndef SECONDS
	$(error SECONDS is not defined)
endif
	sudo ../../../../scripts/RAPL/build/rapl --json "$(JSON)" ../../../../scripts/RAPL/build/time-limiter $(SECONDS) ./binarytrees_run 27
