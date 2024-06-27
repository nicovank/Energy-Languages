#!/bin/bash

echo "Generating input for k-nucleotide/reverse-complement"
node benchmarks/JavaScript/fasta/fasta.js 25000000 > fasta-25000000.txt

echo "Generating input for regex-redux"
node benchmarks/JavaScript/fasta/fasta.js 5000000 > fasta-5000000.txt

echo "Generating input for Fixed-Time's k-nucleotide"
node benchmarks/JavaScript/fasta/fasta.js 800000000 > fasta-800000000.txt
