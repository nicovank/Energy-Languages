ifndef PHP
PHP := php
endif

compile:

run:
	php fannkuchredux.php 12

measure:
ifndef JSON
	$(error JSON is not defined)
endif
ifndef SECONDS
	$(error SECONDS is not defined)
endif
	sudo ../../../../scripts/RAPL/build/time-limiter $(SECONDS) ../../../../scripts/RAPL/build/rapl --json "$(JSON)" php fannkuchredux.php 12

