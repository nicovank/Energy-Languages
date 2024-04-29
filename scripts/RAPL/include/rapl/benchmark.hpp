/*
A thin wrapper to make building benchmarks with runtime/counters/enery
measurements easier. A benchmark file should look like this.

```
// To enable runtime measurements.
#define RAPL_BENCHMARK_RUNTIME 1

// To enable energy measurements.
#define RAPL_BENCHMARK_COUNTERS 1

// To enable energy measurements.
#define RAPL_BENCHMARK_ENERGY 1

// Specify which events to enable.
#define RAPL_BENCHMARK_COUNTERS_EVENTS {{PERF_TYPE_HARDWARE, PERF_COUNT_HW_CPU_CYCLES}}

// Make sure to include header after defining options.
#include <rapl/benchmark.hpp>

void setup(int argc, char **argv) {
    // Initialize the benchmark.
}

void run() {
    // Actual benchmark.
}

void teardown() {
    // Cleanup.
}

int main(int argc, char **argv) {
    const auto result = RAPL_BENCHMARK_MEASURE(argc, argv);
}
```
*/
#pragma once

#include <chrono>
#include <cstdint>
#include <deque>
#include <vector>

#include <glaze/core/common.hpp>

#include <rapl/perf.hpp>

#ifndef RAPL_BENCHMARK_ENERGY_GRANULARITY_MS
#define RAPL_BENCHMARK_ENERGY_GRANULARITY_MS 1000
#endif

#ifndef RAPL_BENCHMARK_RUNTIME_CLOCK
#define RAPL_BENCHMARK_RUNTIME_CLOCK std::chrono::high_resolution_clock
#endif

#ifdef RAPL_BENCHMARK_ENERGY
struct EnergySample {
    TODO_TIME_POINT duration;
    std::uint64_t energy;
};
#endif

struct Result {
#if RAPL_BENCHMARK_RUNTIME
    typename RAPL_BENCHMARK_RUNTIME_CLOCK::rep runtime_ms;
#endif
#if RAPL_BENCHMARK_COUNTERS
    std::vector<std::uint64_t> counters;
#endif
#if RAPL_BENCHMARK_ENERGY
    static_assert(false);
    std::deque<EnergySample> energy_samples;
#endif
};

template <>
struct glz::meta<Result> {
    using T = Result;
    // clang-format off
    [[maybe_unused]] static constexpr auto value =
        std::apply([](auto... args) { return glz::object(args...); }, std::tuple{
#if RAPL_BENCHMARK_RUNTIME
    "runtime_ms", &T::runtime_ms,
#endif
#if RAPL_BENCHMARK_COUNTERS
    "counters", &T::counters,
#endif
#if RAPL_BENCHMARK_ENERGY
    static_assert(false);
    "energy_samples", &T::energy_samples,
#endif
    });
    // clang-format on
};

extern void setup(int argc, char** argv);
extern void run();
extern void teardown();

namespace benchmark {
inline Result measure(int argc, char** argv) {
    Result result;

    setup(argc, argv);

    // Setup measurement infrastructure.
#if RAPL_BENCHMARK_COUNTERS
#ifndef RAPL_BENCHMARK_COUNTERS_EVENTS
#error "RAPL_BENCHMARK_COUNTERS_EVENTS must be defined."
#endif
    perf::Group group(RAPL_BENCHMARK_COUNTERS_EVENTS);
    group.reset();
#endif

    // Actually start measurements.
#if RAPL_BENCHMARK_COUNTERS
    group.enable();
#endif
#if RAPL_BENCHMARK_RUNTIME
    const auto start = RAPL_BENCHMARK_RUNTIME_CLOCK::now();
#endif

    run();

    // Stop measurements.
#if RAPL_BENCHMARK_RUNTIME
    const auto end = RAPL_BENCHMARK_RUNTIME_CLOCK::now();
#endif
#if RAPL_BENCHMARK_COUNTERS
    group.disable();
#endif

// Populate results.
#if RAPL_BENCHMARK_RUNTIME
    result.runtime_ms = std::chrono::duration_cast<std::chrono::milliseconds>(end - start).count();
#endif
#if RAPL_BENCHMARK_COUNTERS
    result.counters = group.read();
#endif

    return result;
}
}; // namespace benchmark

#define RAPL_BENCHMARK_MEASURE(ARGC, ARGV) benchmark::measure(ARGC, ARGV)
