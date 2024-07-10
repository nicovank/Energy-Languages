ifndef PHP
PHP := php
endif

compile:

run:
	php -n nbody.php 1000000000

measure:
ifndef JSON
	$(error JSON is not defined)
endif
ifndef SECONDS
	$(error SECONDS is not defined)
endif
	sudo ../../../../scripts/RAPL/build/rapl --json "$(JSON)" ../../../../scripts/RAPL/build/time-limiter $(SECONDS) php -n nbody.php 1000000000
