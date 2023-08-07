#!/bin/bash
# pwd/cwd should be the folder containing `Energy-Languages`

# Building measurement tool - RAPL
cd Energy-Languages/scripts/RAPL
cmake . -B build -G Ninja -DCMAKE_BUILD_TYPE=Release && cmake --build build

# Performing benchmark
# languages: space-delimited list of programming languages
# n: iteration count of execution under measurement
# warmup: iteration count of execution *before* the measurement
# timeout: maximum time per execution
# o/output: output recorded data (in JSON format)
/usr/bin/python3 scripts/measure.py --languages C C++ Rust Java Go -n 21 --warmup 3 -o data/obelix96/docker-single-core --timeout 600