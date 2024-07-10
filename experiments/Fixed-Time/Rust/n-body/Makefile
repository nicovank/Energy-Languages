-include ../Makefile.defaults

compile:
	RUSTFLAGS="$(RUSTFLAGS) -C llvm-args=-unroll-threshold=500" cargo build --release

run:
	./target/release/n-body 1000000000

measure:
ifndef JSON
	$(error JSON is not defined)
endif
ifndef SECONDS
	$(error SECONDS is not defined)
endif
	sudo ../../../../scripts/RAPL/build/rapl --json "$(JSON)" ../../../../scripts/RAPL/build/time-limiter $(SECONDS) ./target/release/n-body 1000000000
