#include <chrono>
#include <cstdlib>
#include <fstream>
#include <iostream>
#include <mutex>
#include <string>
#include <thread>
#include <tuple>
#include <utility>
#include <vector>

#include <sys/resource.h>
#include <sys/time.h>

#include <glaze/core/common.hpp>
#include <glaze/json/write.hpp>

#include <rapl/cpu.hpp>
#include <rapl/rapl.hpp>
#include <rapl/rusage.hpp>
#include <rapl/utils.hpp>

using Clock = std::chrono::high_resolution_clock;

struct Result {
    Clock::rep runtime;
    rapl::DoubleSample energy;
    struct rusage rusage;
};

int main(int argc, char* argv[]) {
    if (argc < 3) {
        std::cerr << "Usage: ./rapl <json-file> <command> [args...]" << std::endl;
        return 1;
    }

    std::string command = argv[2];
    for (int i = 3; i < argc; ++i) {
        command.append(" ");
        command.append(argv[i]);
    }

    Result result;
    std::vector<rapl::U32Sample> previous;
    std::mutex lock;

    {
        std::lock_guard<std::mutex> guard(lock);
        for (int package = 0; package < cpu::getNPackages(); ++package) {
            previous.emplace_back(rapl::sample(package));
        }
    }

    KillableTimer timer;
    std::thread subprocess = std::thread([&] {
        for (;;) {
            if (!timer.wait(std::chrono::seconds(1))) {
                break;
            }

            std::lock_guard<std::mutex> guard(lock);
            for (int package = 0; package < cpu::getNPackages(); ++package) {
                const auto sample = rapl::sample(package);
                result.energy += rapl::scale(sample - previous[package], package);
                previous[package] = sample;
            }
        }
    });
    ScopeExit _([&] {
        timer.kill();
        subprocess.join();
    });

    struct rusage start_usage;
    struct rusage end_usage;

    if (getrusage(RUSAGE_CHILDREN, &start_usage) != 0) {
        std::cerr << "getrusage failed" << std::endl;
        return 1;
    }
    const auto start = Clock::now();
    const auto status = std::system(command.c_str());
    const auto end = Clock::now();
    if (getrusage(RUSAGE_CHILDREN, &end_usage) != 0) {
        std::cerr << "getrusage failed" << std::endl;
        return 1;
    }

    std::lock_guard<std::mutex> guard(lock);
    for (int package = 0; package < cpu::getNPackages(); ++package) {
        const auto sample = rapl::sample(package);
        result.energy += rapl::scale(sample - previous[package], package);
    }

    if (status != 0) {
        std::cerr << "child process failed" << std::endl;
        return 1;
    }

    result.runtime = std::chrono::duration_cast<std::chrono::milliseconds>(end - start).count();
    result.rusage = end_usage - start_usage;

    if (!(std::ofstream(argv[1], std::ios_base::app) << glz::write_json(result) << "\n")) {
        std::cerr << "write failed" << std::endl;
        return 1;
    }
}
