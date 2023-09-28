# Goals of C-as-C++ experiment
- Because C++ is akin to a superset of C, we decided to measure the performance of C benchmarks when compiled as C++. By changing only the method of compilation, we can observe that there is more to performance than language choice.

# Changes made from the original C benchmarks
- chameneosredux.c
    - In order to compile, in the print_colors function, the color_t variables c1, c2, c3 were changed to int.
- Makefiles
    - Input/output paths were changed
- Makefile.defaults has different flags
    - CC is now set to the g++ compiler (default)
    - Specifies language input with -x flag
    - fpermissive flag is included to turn nonconformant errors into warnings
