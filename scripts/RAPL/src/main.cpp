#include <algorithm>
#include <chrono>
#include <cstdlib>
#include <fstream>
#include <iostream>
#include <string>
#include <vector>

#include <signal.h>
#include <sys/resource.h>
#include <sys/time.h>
#include <sys/types.h>
#include <sys/wait.h>
#include <unistd.h>

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
        {PERF_TYPE_HARDWARE, PERF_COUNT_HW_BRANCH_MISSES}                                                              \
}
// clang-format on

#define RAPL_BENCHMARK_ENERGY 1
#define RAPL_BENCHMARK_ENERGY_GRANULARITY_MS 100

#define RAPL_BENCHMARK_CUSTOM_DATA 1

#include <rapl/benchmark.hpp>

namespace {
std::string json;
std::vector<std::string> command;
bool allowNonZeroExit;
int timeout;

int status;
} // namespace

void setup(int argc, char** argv) {
    auto program = argparse::ArgumentParser("RAPL", "", argparse::default_arguments::help);

    program.add_argument("--json").required().help("the filename where the results are written").metavar("PATH");
    program.add_argument("--allow-non-zero-exit")
        .default_value(false)
        .implicit_value(true)
        .help("allow the child process to exit with a non-zero status code");
    program.add_argument("--timeout")
        .default_value(0)
        .help("amount of time to sleep before killing the child process")
        .metavar("SECONDS")
        .scan<'d', int>();
    program.add_argument("command").required().remaining().help("the command to run").metavar("COMMAND...");

    try {
        program.parse_args(argc, argv);
        json = program.get<std::string>("--json");
        command = program.get<std::vector<std::string>>("command");
        allowNonZeroExit = program.get<bool>("--allow-non-zero-exit");
        timeout = program.get<int>("--timeout");
    } catch (const std::exception& err) {
        std::cerr << err.what() << std::endl;
        std::cerr << program;
        std::exit(EXIT_FAILURE);
    }
}

void run() {
    const auto pid = fork();

    if (pid == -1) {
        std::cerr << "fork failed" << std::endl;
        std::exit(EXIT_FAILURE);
    }

    if (pid == 0) {
        std::vector<char*> c_command;
        std::transform(command.begin(), command.end(), std::back_inserter(c_command),
                       [](const std::string& str) { return const_cast<char*>(str.c_str()); });
        c_command.push_back(nullptr);

        if (execvp(c_command[0], c_command.data()) == -1) {
            std::cerr << "execvp failed" << std::endl;
            std::exit(EXIT_FAILURE);
        }
    }

    // Hack: sleep one second at a time and check for exit status.
    // This saves doing annoying pipe stuff or import a subprocess library.
    if (timeout > 0) {
        const auto start = std::chrono::high_resolution_clock::now();
        while (std::chrono::high_resolution_clock::now() - start < std::chrono::seconds(timeout)) {
            sleep(1);
            if (waitpid(pid, &status, WNOHANG) != 0) {
                return;
            }
        }

        kill(pid, SIGKILL);
    }

    waitpid(pid, &status, 0);
}

void teardown() {
    if (status != 0 && !allowNonZeroExit) {
        std::cerr << "The underlying program failed." << std::endl;
        std::exit(EXIT_FAILURE);
    }
}

int main(int argc, char** argv) {
    auto result = RAPL_BENCHMARK_MEASURE(argc, argv);

    result.custom.emplace("status", std::to_string(status));
    if (!(std::ofstream(json, std::ios_base::app) << glz::write_json(result) << "\n")) {
        std::cerr << "write failed" << std::endl;
        return 1;
    }
}
