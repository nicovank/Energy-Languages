ifndef JAVAC
JAVAC := javac
endif

ifndef JAVA
JAVA := java
endif

compile:
	$(JAVAC) -d . fasta.java

run:
	$(JAVA) fasta 2000000000

measure:
ifndef JSON
	$(error JSON is not defined)
endif
	sudo ../../../../scripts/RAPL/build/rapl --json "$(JSON)" $(JAVA) fasta 2000000000
