-include ../Makefile.defaults

compile:
	RUSTFLAGS="$(RUSTFLAGS) -C llvm-args=-unroll-threshold=500" cargo build --release

run:
	./target/release/n-body 50000000

measure:
ifndef JSON
	$(error JSON is not defined)
endif
	sudo ../../../scripts/RAPL/build/rapl --json "$(JSON)" ./target/release/n-body 50000000
