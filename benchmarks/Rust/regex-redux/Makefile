-include ../Makefile.defaults

compile:
	RUSTFLAGS="$(RUSTFLAGS)" cargo build --release

run:
	./target/release/regex-redux 0 < ../../../fasta-5000000.txt

measure:
ifndef JSON
	$(error JSON is not defined)
endif
	sudo ../../../scripts/RAPL/build/rapl --json "$(JSON)" ./target/release/regex-redux 0 < ../../../fasta-5000000.txt
