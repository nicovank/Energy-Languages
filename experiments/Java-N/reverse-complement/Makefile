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
	sed s/NNNNN/$(NNNNN)/ revcomp.java.in > revcomp.java
	$(JAVAC) -d . revcomp.java

run:
	$(JAVA) revcomp ../../../fasta-25000000.txt 0

measure:
ifndef JSON
	$(error JSON is not defined)
endif
	sudo ../../../scripts/RAPL/build/rapl --json "$(JSON)" $(JAVA) revcomp ../../../fasta-25000000.txt 0
