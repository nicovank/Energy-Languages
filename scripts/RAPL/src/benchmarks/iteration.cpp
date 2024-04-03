#include <chrono>
#include <cstddef>
#include <cstdint>
#include <cstring>
#include <iostream>
#include <random>
#include <thread>
#include <vector>

#include <linux/hw_breakpoint.h>
#include <linux/perf_event.h>
#include <sys/ioctl.h>
#include <sys/syscall.h>
#include <unistd.h>

#include <argparse/argparse.hpp>
#include <benchmark/benchmark.h>

#include <perf.hpp>
#include <rapl.hpp>

#ifndef RAPL_MSR_PKG_SUPPORTED
#error "This tool requires MSR PKG domain support"
#endif

#define CACHE_LINE_SIZE sysconf(_SC_LEVEL3_CACHE_LINESIZE)
#define LL_CACHE_SIZE sysconf(_SC_LEVEL3_CACHE_SIZE)

void work(std::chrono::seconds duration, std::vector<std::uint8_t> memory) {
    std::uint64_t sum = 0;
    std::size_t index = 0;
    auto start = std::chrono::high_resolution_clock::now();
    while (std::chrono::high_resolution_clock::now() - start < duration) {
        for (int i = 0; i < 1'000; ++i) {
            index += CACHE_LINE_SIZE;
            sum += memory[index % memory.size()];
            memory[index % memory.size()] = index;
        }
    }
    benchmark::DoNotOptimize(sum);
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

    program.add_argument("-p", "--miss-rate")
        .required()
        .help("approximate LLC cache miss rate")
        .metavar("P")
        .scan<'g', double>();

    try {
        program.parse_args(argc, argv);
    } catch (const std::exception& err) {
        std::cerr << err.what() << std::endl;
        std::cerr << program;
        return EXIT_FAILURE;
    }

    const auto cores = program.get<std::uint8_t>("cores");
    const auto duration = program.get<std::uint64_t>("duration");
    const auto misses = program.get<double>("miss-rate");

    if (cores == 0) {
        std::cerr << "[ERROR] Can't run a benchmark on zero cores." << std::endl;
        return EXIT_FAILURE;
    }

    if (misses < 0 || misses > 1) {
        std::cerr << "[ERROR] Invalid cache miss percentage." << std::endl;
        return EXIT_FAILURE;
    }

    auto generator = std::default_random_engine(std::random_device()());

    const std::vector<std::pair<int, int>> events
        = {{PERF_TYPE_HARDWARE, PERF_COUNT_HW_CPU_CYCLES},          {PERF_TYPE_HARDWARE, PERF_COUNT_HW_INSTRUCTIONS},
           {PERF_TYPE_HARDWARE, PERF_COUNT_HW_CACHE_REFERENCES},    {PERF_TYPE_HARDWARE, PERF_COUNT_HW_CACHE_MISSES},
           {PERF_TYPE_HARDWARE, PERF_COUNT_HW_BRANCH_INSTRUCTIONS}, {PERF_TYPE_HARDWARE, PERF_COUNT_HW_BRANCH_MISSES},
           {PERF_TYPE_HARDWARE, PERF_COUNT_HW_REF_CPU_CYCLES}};
    perf::Group group(events);

    std::cout << "[INFO] Creating scratch memory..." << std::endl;
    auto memory = std::vector<std::vector<std::uint8_t>>(cores, std::vector<std::uint8_t>(LL_CACHE_SIZE));
    for (auto& buffer : memory) {
        for (auto& byte : buffer) {
            byte = std::uniform_int_distribution<std::uint8_t>()(generator);
        }
    }

    std::cout << "[INFO] Starting benchmark..." << std::endl;
    group.reset();
    group.enable();

    std::vector<std::thread> threads;
    for (std::uint8_t i = 0; i < cores - 1; ++i) {
        threads.emplace_back(work, std::chrono::seconds(duration), std::move(memory.at(i)));
    }
    work(std::chrono::seconds(duration), std::move(memory.back()));
    for (auto& thread : threads) {
        thread.join();
    }

    group.disable();
    const auto counts = group.read();
    for (std::size_t i = 0; i < events.size(); ++i) {
        std::cout << perf::toString(events[i].first, events[i].second) << ": " << counts[i] << std::endl;
    }
}
