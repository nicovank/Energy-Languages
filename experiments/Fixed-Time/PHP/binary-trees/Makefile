ifndef PHP
PHP := php
endif

compile:

run:
	php -n -d memory_limit=4096M binarytrees.php 27

measure:
ifndef JSON
	$(error JSON is not defined)
endif
ifndef SECONDS
	$(error SECONDS is not defined)
endif
	sudo ../../../../scripts/RAPL/build/time-limiter $(SECONDS) ../../../../scripts/RAPL/build/rapl --json "$(JSON)" php -n -d memory_limit=4096M binarytrees.php 27
