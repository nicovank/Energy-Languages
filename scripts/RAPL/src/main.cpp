#include <algorithm>
#include <cstdlib>
#include <fstream>
#include <iostream>
#include <string>
#include <vector>

#include <sys/resource.h>
#include <sys/time.h>

#include <argparse/argparse.hpp>
#include <glaze/json/write.hpp>

#define RAPL_BENCHMARK_RUNTIME 1

#define RAPL_BENCHMARK_RUSAGE 1
#define RAPL_BENCHMARK_RUSAGE_WHO RUSAGE_CHILDREN

#define RAPL_BENCHMARK_COUNTERS 1
#include <linux/perf_event.h>
// clang-format off
#define RAPL_BENCHMARK_COUNTERS_EVENTS {                                                                               \
        {PERF_TYPE_HARDWARE, PERF_COUNT_HW_CPU_CYCLES},                                                                \
        {PERF_TYPE_HARDWARE, PERF_COUNT_HW_INSTRUCTIONS},                                                              \
        {PERF_TYPE_HARDWARE, PERF_COUNT_HW_CACHE_REFERENCES},                                                          \
        {PERF_TYPE_HARDWARE, PERF_COUNT_HW_CACHE_MISSES},                                                              \
        {PERF_TYPE_HARDWARE, PERF_COUNT_HW_BRANCH_INSTRUCTIONS},                                                       \
        {PERF_TYPE_HARDWARE, PERF_COUNT_HW_BRANCH_MISSES},                                                             \
        {PERF_TYPE_SOFTWARE, PERF_COUNT_SW_TASK_CLOCK}                                                                 \
}
// clang-format on

#define RAPL_BENCHMARK_ENERGY 1
#define RAPL_BENCHMARK_ENERGY_GRANULARITY_MS 100

#include <rapl/benchmark.hpp>

namespace {
std::string json;
std::string command;
int status;
} // namespace

void setup(int argc, char** argv) {
    auto program = argparse::ArgumentParser("RAPL", "", argparse::default_arguments::help);

    program.add_argument("--json").required().help("the filename where the results are written").metavar("PATH");
    program.add_argument("command").required().remaining().help("the command to run").metavar("COMMAND...");

    try {
        program.parse_args(argc, argv);
        json = program.get<std::string>("--json");
        // FIXME C++23: Use std::ranges::views::join_with.
        const auto parts = program.get<std::vector<std::string>>("command");
        command = std::accumulate(parts.begin(), parts.end(), std::string(),
                                  [](const auto& a, const auto& b) { return a + " " + b; });
    } catch (const std::exception& err) {
        std::cerr << err.what() << std::endl;
        std::cerr << program;
        std::exit(EXIT_FAILURE);
    }
}

void run() {
    status = std::system(command.c_str());
}

void teardown() {
    if (status != 0) {
        std::cerr << "The underlying program failed." << std::endl;
        std::exit(EXIT_FAILURE);
    }
}

int main(int argc, char** argv) {
    [[maybe_unused]] const auto result = RAPL_BENCHMARK_MEASURE(argc, argv);

    if (!(std::ofstream(json, std::ios_base::app) << glz::write_json(result) << "\n")) {
        std::cerr << "write failed" << std::endl;
        return 1;
    }
}
