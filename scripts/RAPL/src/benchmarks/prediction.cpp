#include <algorithm>
#include <cstdint>
#include <cstdlib>
#include <deque>
#include <iostream>
#include <random>
#include <utility>
#include <vector>

#include <cstdlib>

#include <argparse/argparse.hpp>
#include <benchmark/benchmark.h>
#include <fmt/core.h>

#define RAPL_BENCHMARK_RUNTIME 1

#define RAPL_BENCHMARK_COUNTERS 1

// clang-format off
#include <linux/perf_event.h>
#define RAPL_BENCHMARK_COUNTERS_EVENTS {                                                                               \
        {PERF_TYPE_HARDWARE, PERF_COUNT_HW_CPU_CYCLES},                                                                \
        {PERF_TYPE_HARDWARE, PERF_COUNT_HW_BRANCH_INSTRUCTIONS},                                                       \
        {PERF_TYPE_HARDWARE, PERF_COUNT_HW_BRANCH_MISSES}                                                              \
}
// clang-format on

#include <rapl/benchmark.hpp>

namespace {
std::uint64_t n;
std::uint64_t iterations;

std::vector<std::uint64_t> a;
std::vector<std::uint64_t> b;
/* std::vector<bool> */ std::deque<std::uint64_t> c;
}; // namespace

void setup(int argc, char** argv) {
    auto program = argparse::ArgumentParser("benchmark", "", argparse::default_arguments::help);

    program.add_argument("-n")
        .required()
        .help("a measure on how much work to do in each iteration")
        .metavar("N")
        .scan<'d', std::uint64_t>();

    program.add_argument("-i", "--iterations")
        .required()
        .help("the number of iterations")
        .metavar("N")
        .scan<'d', std::uint64_t>();

    program.add_argument("-p")
        .required()
        .help("the probability of taking the true branch")
        .metavar("P")
        .scan<'g', double>();

    try {
        program.parse_args(argc, argv);
    } catch (const std::exception& err) {
        std::cerr << err.what() << std::endl;
        std::cerr << program;
        exit(EXIT_FAILURE);
    }

    n = program.get<std::uint64_t>("n");
    iterations = program.get<std::uint64_t>("iterations");
    const auto p = program.get<double>("p");

    auto generator = std::mt19937_64(std::random_device()());

    a.resize(n);
    std::generate(a.begin(), a.end(),
                  [&generator]() { return std::uniform_int_distribution<std::uint64_t>()(generator); });
    b.resize(n);
    std::generate(b.begin(), b.end(),
                  [&generator]() { return std::uniform_int_distribution<std::uint64_t>()(generator); });

    c.resize(iterations);
    std::generate(c.begin(), c.end(), [p, &generator]() { return std::bernoulli_distribution(p)(generator); });
}

void run() {
    std::uint64_t sum = 0;
    for (std::uint64_t i = 0; i < iterations; ++i) {
        if (c[i]) {
            for (std::uint64_t j = 0; j < n; ++j) {
                a[j] += (i * 13) ^ (j * 71);
                sum += a[j] ^ (b[j] << 3);
            }
        } else {
            for (std::uint64_t j = 0; j < n; ++j) {
                b[j] += (i * 71) ^ (j * 13);
                sum += (a[j] << 3) ^ b[j];
            }
        }
    }
    benchmark::DoNotOptimize(sum);
}

void teardown() {}

int main(int argc, char** argv) {
    const auto result = RAPL_BENCHMARK_MEASURE(argc, argv);

    const auto events = std::vector<std::pair<int, int>>(RAPL_BENCHMARK_COUNTERS_EVENTS);

    std::cout << "Runtime: " << result.runtime_ms << std::endl;
    for (std::size_t i = 0; i < events.size(); ++i) {
        std::cout << perf::toString(events.at(i)) << ": " << result.counters[i] << std::endl;
    }
}
