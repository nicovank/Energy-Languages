#include <chrono>
#include <condition_variable>
#include <cstdlib>
#include <cstring>
#include <fstream>
#include <ios>
#include <iostream>
#include <mutex>
#include <ratio>
#include <thread>
#include <vector>

#include <linux/hw_breakpoint.h>
#include <linux/perf_event.h>
#include <sys/ioctl.h>
#include <sys/syscall.h>
#include <unistd.h>

#include <cpu.hpp>
#include <msr.hpp>

struct KillableWait {
    template <typename Rep, typename Period>
    bool wait(const std::chrono::duration<Rep, Period>& time) {
        std::unique_lock<std::mutex> lock(mutex);
        return !cv.wait_for(lock, time, [&] { return killed; });
    }

    void kill() {
        std::unique_lock<std::mutex> lock(mutex);
        killed = true;
        cv.notify_all();
    }

  private:
    std::mutex mutex;
    std::condition_variable cv;
    bool killed = false;
};

void aggregate(msr::Sample& total, const msr::Sample& sample) {
    total.pkg += sample.pkg;
    total.pp0 += sample.pp0;
    total.pp1 += sample.pp1;
    total.dram += sample.dram;
    total.psys += sample.psys;
}

using Clock = std::chrono::high_resolution_clock;

int main(int argc, char* argv[]) {
    if (argc < 3) {
        std::cerr << "Usage: ./rapl <csv> '<command> [args...]'" << std::endl;
        return 1;
    }

    struct perf_event_attr pe;
    memset(&pe, 0, sizeof(struct perf_event_attr));
    pe.type = PERF_TYPE_HARDWARE;
    pe.config = PERF_COUNT_HW_CPU_CYCLES;
    pe.size = sizeof(struct perf_event_attr);
    pe.inherit = 1;
    pe.disabled = 1;

    const auto fd = syscall(__NR_perf_event_open, &pe, 0, -1, -1, 0);
    if (fd == -1) {
        std::cerr << "perf_event_open failed" << std::endl;
        return 1;
    }
    ioctl(fd, PERF_EVENT_IOC_RESET, 0);

    msr::Sample total;
    std::vector<msr::Sample> previous;
    std::mutex previous_lock;

    for (int package = 0; package < cpu::getNPackages(); ++package) {
        previous.emplace_back(msr::sample(package));
    }

    KillableWait timer;
    std::thread subprocess = std::thread([&]() {
        for (;;) {
            using namespace std::chrono_literals;
            if (!timer.wait(10s)) {
                break;
            }

            std::lock_guard<std::mutex> guard(previous_lock);
            for (int package = 0; package < cpu::getNPackages(); ++package) {
                const auto sample = msr::sample(package);
                aggregate(total, msr::delta(previous[package], sample));
                previous[package] = sample;
            }
        }
    });

    ioctl(fd, PERF_EVENT_IOC_ENABLE, 0);
    const auto start = Clock::now();
    const auto status = system(argv[2]);
    const auto end = Clock::now();
    ioctl(fd, PERF_EVENT_IOC_DISABLE, 0);

    uint64_t cycles;
    if (read(fd, &cycles, sizeof(uint64_t)) != sizeof(uint64_t)) {
        std::cerr << "read failed" << std::endl;
        return 1;
    }

    if (status != 0) {
        return 1;
    }

    std::lock_guard<std::mutex> guard(previous_lock);
    for (int package = 0; package < cpu::getNPackages(); ++package) {
        const auto sample = msr::sample(package);
        aggregate(total, msr::delta(previous[package], sample));
    }

    const auto elapsed = std::chrono::duration_cast<std::chrono::milliseconds>(end - start).count();

    std::ofstream file(argv[1], std::ios_base::app);
    file << elapsed << ",";
    file << total.pkg << ",";
    file << total.pp0 << ",";
    file << total.pp1 << ",";
    file << total.dram << ",";
    file << total.psys << ",";
    file << cycles << std::endl;

    timer.kill();
    subprocess.join();
}
