ifndef JAVAC
JAVAC := javac
endif

ifndef JAVA
JAVA := java
endif

compile:
ifndef NNNNN
	$(error NNNNN is not defined)
endif
	sed s/NNNNN/$(NNNNN)/ regexredux.java.in > regexredux.java
	$(JAVAC) -d . regexredux.java

run:
	$(JAVA) regexredux ../../../fasta-5000000.txt 0

measure:
ifndef JSON
	$(error JSON is not defined)
endif
	sudo ../../../scripts/RAPL/build/rapl --json "$(JSON)" $(JAVA) regexredux ../../../fasta-5000000.txt 0
