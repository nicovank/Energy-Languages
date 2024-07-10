ifndef PYTHON
PYTHON := python3
endif

compile:
	$(PYTHON) -m compileall -o 2 mandelbrot.py

run:
	$(PYTHON) -OO mandelbrot.py 16000

measure:
ifndef JSON
	$(error JSON is not defined)
endif
ifndef SECONDS
	$(error SECONDS is not defined)
endif
	sudo ../../../../scripts/RAPL/build/time-limiter $(SECONDS) ../../../../scripts/RAPL/build/rapl --json "$(JSON)" $(PYTHON) -OO mandelbrot.py 16000
