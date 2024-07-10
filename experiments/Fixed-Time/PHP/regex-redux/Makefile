ifndef PHP
PHP := php
endif

compile:

run:
	php -d memory_limit=512M regexredux.php 0 < ../../../../fasta-5000000.txt

measure:
ifndef JSON
	$(error JSON is not defined)
endif
ifndef SECONDS
	$(error SECONDS is not defined)
endif
	sudo ../../../../scripts/RAPL/build/rapl --json "$(JSON)" ../../../../scripts/RAPL/build/time-limiter $(SECONDS) php -d memory_limit=512M regexredux.php 0 < ../../../../fasta-5000000.txt
