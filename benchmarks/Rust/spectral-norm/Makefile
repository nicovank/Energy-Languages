-include ../Makefile.defaults

compile:
	RUSTFLAGS="$(RUSTFLAGS)" cargo build --release

run:
	./target/release/spectral-norm 5500

measure:
ifndef JSON
	$(error JSON is not defined)
endif
	sudo ../../scripts/RAPL/build/rapl --json "$(JSON)" ./target/release/spectral-norm 5500
