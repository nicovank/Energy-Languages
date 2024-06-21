ifndef JAVAC
JAVAC := javac
endif

ifndef JAVA
JAVA := java
endif

compile:
	$(JAVAC) -d . mandelbrot.java

run:
	$(JAVA) mandelbrot 16000

measure:
ifndef JSON
	$(error JSON is not defined)
endif
	sudo ../../../../scripts/RAPL/build/rapl --json "$(JSON)" $(JAVA) mandelbrot 16000
