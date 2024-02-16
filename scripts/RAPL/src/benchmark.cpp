#include <chrono>
#include <cstdint>
#include <iostream>
#include <thread>
#include <vector>

#include <argparse/argparse.hpp>
#include <benchmark/benchmark.h>

#include <rapl.hpp>

#ifndef RAPL_MSR_PKG_SUPPORTED
#error "This tool requires MSR PKG domain support"
#endif

void work(std::chrono::seconds duration) {
    auto start = std::chrono::high_resolution_clock::now();
    while (std::chrono::high_resolution_clock::now() - start < duration) {
        for (int i = 0; i < 1'000; ++i) {
            benchmark::DoNotOptimize(i);
        }
    }
}

int main(int argc, char** argv) {
    auto program = argparse::ArgumentParser("benchmark", "", argparse::default_arguments::help);

    program.add_argument("-c", "--cores")
        .required()
        .help("the number of cores to run the benchmark on")
        .metavar("N")
        .scan<'d', std::uint8_t>();

    program.add_argument("-d", "--duration")
        .required()
        .help("approximate duration to run for in seconds")
        .metavar("SECONDS")
        .scan<'d', std::uint64_t>();

    try {
        program.parse_args(argc, argv);
    } catch (const std::exception& err) {
        std::cerr << err.what() << std::endl;
        std::cerr << program;
        return EXIT_FAILURE;
    }

    auto cores = program.get<std::uint8_t>("cores");
    auto duration = program.get<std::uint64_t>("duration");

    if (cores == 0) {
        std::cerr << "[ERROR] Can't ran a benchmark on zero cores!" << std::endl;
        return EXIT_FAILURE;
    }

    if (cores == 1) {
        work(std::chrono::seconds(duration));
    } else {
        std::vector<std::thread> threads;
        for (std::uint8_t i = 0; i < cores; ++i) {
            threads.emplace_back(work, std::chrono::seconds(duration));
        }
        for (auto& thread : threads) {
            thread.join();
        }
    }

    std::cout << "Time: " << duration << " seconds" << std::endl;
}
