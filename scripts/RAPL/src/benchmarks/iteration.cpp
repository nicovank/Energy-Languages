#include <algorithm>
#include <chrono>
#include <cstdint>
#include <cstdlib>
#include <iomanip>
#include <iostream>
#include <numeric>
#include <random>
#include <thread>
#include <vector>

#include <argparse/argparse.hpp>
#include <benchmark/benchmark.h>

#define RAPL_BENCHMARK_RUNTIME 1

#define RAPL_BENCHMARK_COUNTERS 1

#define RAPL_BENCHMARK_ENERGY 1

#include <linux/perf_event.h>
// clang-format off
#define RAPL_BENCHMARK_COUNTERS_EVENTS {                                                                               \
        {PERF_TYPE_HARDWARE, PERF_COUNT_HW_CACHE_REFERENCES},                                                          \
        {PERF_TYPE_HARDWARE, PERF_COUNT_HW_CACHE_MISSES},                                                              \
        {PERF_TYPE_SOFTWARE, PERF_COUNT_SW_TASK_CLOCK}                                                                 \
}
// clang-format on

#include <rapl/benchmark.hpp>

namespace {
std::uint8_t cores;
std::uint64_t iterations;
std::vector<std::vector<std::uint64_t>> memory;
}; // namespace

void setup(int argc, char** argv) {
    auto program = argparse::ArgumentParser("benchmark", "", argparse::default_arguments::help);

    program.add_argument("-c", "--cores")
        .required()
        .help("the number of threads to run")
        .metavar("N")
        .scan<'d', std::uint8_t>();

    program.add_argument("-i", "--iterations")
        .required()
        .help("number of iterations to run on each thread")
        .metavar("N")
        .scan<'d', std::uint64_t>();

    program.add_argument("-n", "--number-objects")
        .required()
        .help("the number of objects (std::uint_64) to use for each thread")
        .metavar("N")
        .scan<'d', std::uint64_t>();

    try {
        program.parse_args(argc, argv);
    } catch (const std::exception& err) {
        std::cerr << err.what() << std::endl;
        std::cerr << program;
        std::exit(EXIT_FAILURE);
    }

    cores = program.get<std::uint8_t>("cores");
    iterations = program.get<std::uint64_t>("iterations");
    const auto n = program.get<std::uint64_t>("number-objects");

    if (cores == 0) {
        std::cerr << "[ERROR] Can't run a benchmark on zero cores." << std::endl;
        std::exit(EXIT_FAILURE);
    }

    if (n == 0) {
        std::cerr << "[ERROR] Need at least one allocation." << std::endl;
        std::exit(EXIT_FAILURE);
    }

    auto generator = std::default_random_engine(std::random_device()());

    memory.resize(cores);
    for (auto& buffer : memory) {
        for (std::uint64_t i = 0; i < n; ++i) {
            buffer.push_back(std::uniform_int_distribution<std::uint64_t>()(generator));
        }
    }
}

void work(std::uint64_t iterations, std::vector<std::uint64_t> memory) {
    std::uint64_t sum = 0;
    for (std::size_t i = 0; i < iterations; ++i) {
        sum += memory[i % memory.size()];
    }
    benchmark::DoNotOptimize(sum);
}

void run() {
    std::vector<std::thread> threads;
    for (std::uint8_t i = 0; i < cores - 1; ++i) {
        threads.emplace_back(work, iterations, std::move(memory.at(i)));
    }
    work(iterations, std::move(memory.back()));
    for (auto& thread : threads) {
        thread.join();
    }
}

void teardown() {}

int main(int argc, char** argv) {
    const auto result = RAPL_BENCHMARK_MEASURE(argc, argv);

    if (result.runtime_ms == 0) {
        std::cerr << "[ERROR] Runtime was zero, please increase iterations." << std::endl;
        return EXIT_FAILURE;
    }

    const auto task_clock_it = std::find_if(result.counters.begin(), result.counters.end(), [&](const auto& counter) {
        return counter.first == "PERF_COUNT_SW_TASK_CLOCK";
    });
    assert(task_clock_it != result.counters.end());

    const auto cache_misses_it = std::find_if(result.counters.begin(), result.counters.end(), [&](const auto& counter) {
        return counter.first == "PERF_COUNT_HW_CACHE_MISSES";
    });
    assert(cache_misses_it != result.counters.end());

    const auto cache_references_it
        = std::find_if(result.counters.begin(), result.counters.end(),
                       [&](const auto& counter) { return counter.first == "PERF_COUNT_HW_CACHE_REFERENCES"; });
    assert(cache_references_it != result.counters.end());

    double total_pkg_energy = 0;
    double total_dram_energy = 0;

    for (const auto& sample : result.energy_samples) {
        for (const auto& package : sample.energy) {
            total_pkg_energy += package.pkg;
            total_dram_energy += package.dram;
        }
    }

    std::cout << std::fixed << std::setprecision(2);
    // std::cout << "Total runtime: " << result.runtime_ms << " ms" << std::endl;
    // std::cout << "Average number of active cores: "
    //           << (static_cast<double>(task_clock_it->second) / 1e6) / result.runtime_ms << std::endl;
    // std::cout << "LLC misses: " << cache_misses_it->second << std::endl;
    // std::cout << "LLC misses per second: " << cache_misses_it->second / result.runtime_ms * 1e3 << std::endl;
    // std::cout << "LLC miss rate: " << 100 * static_cast<double>(cache_misses_it->second) /
    // cache_references_it->second
    //           << "%" << std::endl;
    // std::cout << "Average power draw (PKG): " << total_pkg_energy / result.runtime_ms * 1e3 << " W" << std::endl;
    // std::cout << "Average power draw (DRAM): " << total_dram_energy / result.runtime_ms * 1e3 << " W" << std::endl;

    std::cout << "(" << 100 * static_cast<double>(cache_misses_it->second) / cache_references_it->second << ", "
              << ((static_cast<double>(task_clock_it->second) / 1e6) / result.runtime_ms) << ", "
              << (cache_misses_it->second / result.runtime_ms * 1e3) << ", "
              << (total_pkg_energy / result.runtime_ms * 1e3) << ", " << total_dram_energy / result.runtime_ms * 1e3
              << ")"
              << "," << std::endl;
}
