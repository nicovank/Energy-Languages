ifndef JAVAC
JAVAC := javac
endif

ifndef JAVA
JAVA := java
endif

compile:
	$(JAVAC) -d . fannkuchredux.java

run:
	$(JAVA) fannkuchredux 12

measure:
ifndef JSON
	$(error JSON is not defined)
endif
ifndef SECONDS
	$(error SECONDS is not defined)
endif
	sudo ../../../../scripts/RAPL/build/rapl --json "$(JSON)" ../../../../scripts/RAPL/build/time-limiter $(SECONDS) $(JAVA) fannkuchredux 12
