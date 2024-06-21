ifndef PHP
PHP := php
endif

compile:

run:
	php -n spectralnorm.php 150000

measure:
ifndef JSON
	$(error JSON is not defined)
endif
	sudo ../../../scripts/RAPL/build/rapl --json "$(JSON)" php -n spectralnorm.php 150000
