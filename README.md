# Energy Efficiency in Programming Languages

[Nicolas van Kempen](https://nvankempen.com), [Emery Berger](https://emeryberger.com),
Hyuk-Je Kwon, and Dung Tuan Nguyen.

This repository contains our code and experiments reproducing and investigating _[Energy efficiency across programming languages: how do energy, time, and memory relate?](https://dl.acm.org/doi/10.1145/3136014.3136031)_.

## Documentation

### Requirements

Running the measurement tool requires:
 -  an Intel processor with RAPL support.
 -  Linux (tested on Ubuntu 22.04).

### Docker

The easiest way to run these benchmarks is using Docker.
```bash
% sudo modprobe msr # Enable msr kernel module.
% sudo python3 -m scripts.build_docker_image
% sudo docker run --privileged -v [OUTPUT_DIRECTORY]:/root/data energy-languages [OPTIONS]
```

The following options are available:
 -  `--languages`: A whitespace-separated list of languages to benchmarks.
 -  `--warmup`: The number of warmup iterations to run before measuring.
 -  `--iterations`: The number of iterations to run for each benchmark.
 -  `--timeout`: The timeout after which to stop execution. Some benchmarks are known to occasionally run indefinitely.

Here is an example running all languages/benchmarks pairs.
```bash
% sudo docker run -it --rm --privileged -v `pwd`/data/`hostname -s`/docker-default:/root/data energy-languages \
    --languages C C++ Rust Go Java C\# JavaScript TypeScript PHP Python PyPy Lua LuaJIT \
    --warmup 1 \
    --iterations 21 \
    --timeout 10000
```

Running additional experiments.
```bash
% sudo docker run -it --rm --privileged -v `pwd`/data/`hostname -s`/docker-default:/root/data energy-languages \
    --benchmark-root experiments \
    --languages "C as C++" "Go-no-GC" "JavaScript as TypeScript" \
    --warmup 1 \
    --iterations 21 \
    --timeout 10000
```

Running Java-N experiments.
```bash
% sudo ./scripts/docker-java-n.sh Java docker-default
```

## License

The original benchmark suite, the
[Computer Language Benchmark Game](https://benchmarksgame-team.pages.debian.net/benchmarksgame/), is under
[BSD-3-Clause](https://salsa.debian.org/benchmarksgame-team/benchmarksgame/-/blob/master/LICENSE.md).

Code from [the repository this one originally forked from](https://github.com/greensoftwarelab/Energy-Languages) is
under [MIT](https://github.com/greensoftwarelab/Energy-Languages/blob/master/LICENSE).

Any other code in this repository is under [Apache-2.0](LICENSE).
