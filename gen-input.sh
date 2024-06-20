#!/bin/bash

echo "Generating input for k-nucleotide/reverse-complement"
node benchmarks/JavaScript/fasta/fasta.js 25000000 > knucleotide-input25000000.txt
cp knucleotide-input25000000.txt revcomp-input25000000.txt

echo "Generating input for regex-redux"
node benchmarks/JavaScript/fasta/fasta.js 5000000 > regexredux-input5000000.txt

echo "Generating input for Fixed-Time's k-nucleotide"
node benchmarks/JavaScript/fasta/fasta.js 800000000 > knucleotide-input800000000.txt
