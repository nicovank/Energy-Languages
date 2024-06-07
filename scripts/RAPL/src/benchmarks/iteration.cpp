#include <algorithm>
#include <chrono>
#include <cstdint>
#include <cstdlib>
#include <iostream>
#include <numeric>
#include <random>
#include <thread>
#include <vector>

#include <argparse/argparse.hpp>
#include <benchmark/benchmark.h>

#define RAPL_BENCHMARK_RUNTIME 1

#define RAPL_BENCHMARK_RUSAGE 1

#define RAPL_BENCHMARK_COUNTERS 1

#define RAPL_BENCHMARK_ENERGY 1

#include <linux/perf_event.h>
// clang-format off
#define RAPL_BENCHMARK_COUNTERS_EVENTS {                                                                               \
        {PERF_TYPE_HARDWARE, PERF_COUNT_HW_CPU_CYCLES},                                                                \
        {PERF_TYPE_HARDWARE, PERF_COUNT_HW_INSTRUCTIONS},                                                              \
        {PERF_TYPE_HARDWARE, PERF_COUNT_HW_CACHE_REFERENCES},                                                          \
        {PERF_TYPE_HARDWARE, PERF_COUNT_HW_CACHE_MISSES},                                                              \
        {PERF_TYPE_HARDWARE, PERF_COUNT_HW_BRANCH_INSTRUCTIONS},                                                       \
        {PERF_TYPE_HARDWARE, PERF_COUNT_HW_BRANCH_MISSES},                                                             \
        {PERF_TYPE_HARDWARE, PERF_COUNT_HW_REF_CPU_CYCLES}                                                             \
}
// clang-format on

#include <rapl/benchmark.hpp>

namespace {
std::uint8_t cores;
std::uint64_t duration;
std::vector<std::vector<std::uint64_t>> memory;
}; // namespace

void setup(int argc, char** argv) {
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

    program.add_argument("-n", "--number-objects")
        .required()
        .help("the number of objects to use")
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
    duration = program.get<std::uint64_t>("duration");
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

void work(std::chrono::seconds duration, std::vector<std::uint64_t> memory) {
    std::uint64_t sum = 0;
    auto start = std::chrono::high_resolution_clock::now();
    for (std::size_t i = 0; std::chrono::high_resolution_clock::now() - start < duration; ++i) {
        sum += (i ^ memory[i % memory.size()]) + 13 * i;
        memory[i % memory.size()] = sum;
    }
    benchmark::DoNotOptimize(sum);
}

void run() {
    std::vector<std::thread> threads;
    for (std::uint8_t i = 0; i < cores - 1; ++i) {
        threads.emplace_back(work, std::chrono::seconds(duration), std::move(memory.at(i)));
    }
    work(std::chrono::seconds(duration), std::move(memory.back()));
    for (auto& thread : threads) {
        thread.join();
    }
}

void teardown() {}

int main(int argc, char** argv) {
    const auto result = RAPL_BENCHMARK_MEASURE(argc, argv);

    std::cout << "Total runtime: " << result.runtime_ms << " ms" << std::endl;
    std::cout << "CPU utilization: "
              << ((result.rusage.ru_utime.tv_sec + result.rusage.ru_stime.tv_sec
                   + 1e-6 * (result.rusage.ru_utime.tv_usec + result.rusage.ru_stime.tv_usec))
                  / (1e-3 * result.runtime_ms))
              << std::endl;
    const auto energy = std::accumulate(result.energy_samples.begin(), result.energy_samples.end(), 0.0,
                                        [](double sum, const auto& sample) { return sum + sample.energy.pkg; });
    std::cout << "Energy consumed: " << energy << " J" << std::endl;
}
