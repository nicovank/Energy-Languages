ifndef PHP
PHP := php
endif

compile:

run:
	php -n -d memory_limit=1024M revcomp.php 0 < ../../../fasta-25000000.txt

measure:
ifndef JSON
	$(error JSON is not defined)
endif
	sudo ../../../scripts/RAPL/build/rapl --json "$(JSON)" php -n -d memory_limit=1024M revcomp.php 0 < ../../../fasta-25000000.txt
