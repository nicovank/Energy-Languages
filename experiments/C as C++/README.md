# Goals of C-as-C++ experiment
- Because C++ is akin to a superset of C, we decided to measure the performance of C benchmarks when compiled as C++. By changing only the method of compilation, we can observe that there is more to performance than language choice.

# Changes made from the original C benchmarks
### chameneosredux.c
```
93c93,95
<     int c1, c2, c3;
---
>     enum color_t                c1;
>     enum color_t                c2;
>     enum color_t                c3;
```
### Makefiles
- All output paths changed for "make measure" and input paths changed for benchmarks that require file input.
```
# Example: binary-trees/Makefile
13c13
< 	sudo ../../../scripts/RAPL/build/rapl "$(JSON)" ./binarytrees_run 21
---
> 	sudo ../../scripts/RAPL/build/rapl "$(JSON)" ./binarytrees_run 21
```
```
# Example: k-nucleotide/Makefile
8c8
< 	./knucleotide_run 0 < ../../../knucleotide-input25000000.txt
---
> 	./knucleotide_run 0 < ../../knucleotide-input25000000.txt
14c14
< 	sudo ../../../scripts/RAPL/build/rapl "$(JSON)" ./knucleotide_run 0 < ../../../knucleotide-input25000000.txt
---
> 	sudo ../../scripts/RAPL/build/rapl "$(JSON)" ./knucleotide_run 0 < ../../knucleotide-input25000000.txt
```
### Makefile.defaults
- CC is now set to the g++ compiler (default)
- Specifies language input with -x flag
- fpermissive flag is included to turn nonconformant errors into warnings, without which the following benchmarks would not compile:
    - chameneos-redux
    - k-nucleotide
    - mandelbrot
    - regex-redux
    - reverse-complement
    - spectral-norm
