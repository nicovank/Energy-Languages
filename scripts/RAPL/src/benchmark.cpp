#include <chrono>
#include <cstdint>
#include <cstring>
#include <iostream>
#include <memory>
#include <thread>
#include <vector>

#include <linux/hw_breakpoint.h>
#include <linux/perf_event.h>
#include <sys/ioctl.h>
#include <sys/syscall.h>
#include <unistd.h>

#include <argparse/argparse.hpp>
#include <benchmark/benchmark.h>

#include <rapl.hpp>

#ifndef RAPL_MSR_PKG_SUPPORTED
#error "This tool requires MSR PKG domain support"
#endif

static std::unique_ptr<std::vector<std::uint8_t>> memory;

void work(std::chrono::seconds duration) {
    auto start = std::chrono::high_resolution_clock::now();
    while (std::chrono::high_resolution_clock::now() - start < duration) {
        for (int i = 0; i < 1'000; ++i) {
            benchmark::DoNotOptimize(i);
        }
    }
}

namespace perf {
int perf_event_open(struct perf_event_attr* attr, pid_t pid, int cpu, int group_fd, unsigned long flags) {
    return syscall(__NR_perf_event_open, attr, pid, cpu, group_fd, flags);
}

// Cache event only, TODO later.
struct CountingEvent {
    explicit CountingEvent(std::uint32_t type, std::uint64_t config) {
        struct perf_event_attr attr;
        std::memset(&attr, 0, sizeof(struct perf_event_attr));
        attr.type = type;
        attr.size = sizeof(struct perf_event_attr);
        attr.config = config;
        attr.disabled = 1;
        attr.inherit = 1;

        fd = perf_event_open(&attr, 0, -1, -1, 0);
        if (fd == -1) {
            std::cerr << "[ERROR] Failed to open perf event: " << strerror(errno) << std::endl;
            std::exit(EXIT_FAILURE);
        }
        assert(fd != -1);
    }

    ~CountingEvent() {
        close(fd);
    }

    CountingEvent(const CountingEvent&) = delete;
    CountingEvent(CountingEvent&&) = default;
    CountingEvent& operator=(const CountingEvent&) = delete;
    CountingEvent& operator=(CountingEvent&&) = default;

    void reset() {
        const auto status = ioctl(fd, PERF_EVENT_IOC_RESET, 0);
        assert(status == 0);
    }

    void enable() {
        const auto status = ioctl(fd, PERF_EVENT_IOC_ENABLE, 0);
        assert(status == 0);
    }

    void disable() {
        const auto status = ioctl(fd, PERF_EVENT_IOC_DISABLE, 0);
        assert(status == 0);
    }

    std::uint64_t read() const {
        std::uint64_t count;
        const auto status = ::read(fd, &count, sizeof(std::uint64_t));
        assert(status == sizeof(std::uint64_t));
        return count;
    }

  private:
    int fd;
};

// Would love to use PERF_FORMAT_GROUP but it messes with inherit.
struct EventGroup {
    // EventGroup(std::vector<Event> events) : events(std::move(events)) {}

    EventGroup(std::vector<std::pair<std::uint32_t, std::uint64_t>> definitions) {
        events.reserve(definitions.size());
        for (const auto& [type, config] : definitions) {
            events.emplace_back(type, config);
        }
    }

    void reset() {
        for (auto& event : events) {
            event.reset();
        }
    }

    void enable() {
        for (auto& event : events) {
            event.enable();
        }
    }

    void disable() {
        for (auto& event : events) {
            event.disable();
        }
    }

    std::vector<std::uint64_t> read() const {
        std::vector<std::uint64_t> counts;
        counts.reserve(events.size());
        for (const auto& event : events) {
            counts.push_back(event.read());
        }
        return counts;
    }

  private:
    std::vector<CountingEvent> events;
};
} // namespace perf

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

    program.add_argument("--percentage-misses")
        .required()
        .help("approximate LLC cache miss percentage")
        .metavar("SECONDS")
        .scan<'g', double>();

    try {
        program.parse_args(argc, argv);
    } catch (const std::exception& err) {
        std::cerr << err.what() << std::endl;
        std::cerr << program;
        return EXIT_FAILURE;
    }

    auto cores = program.get<std::uint8_t>("cores");
    auto duration = program.get<std::uint64_t>("duration");
    auto misses = program.get<double>("percentage-misses");

    if (cores == 0) {
        std::cerr << "[ERROR] Can't run a benchmark on zero cores." << std::endl;
        return EXIT_FAILURE;
    }

    if (misses < 0 || misses > 1) {
        std::cerr << "[ERROR] Invalid cache miss percentage." << std::endl;
        return EXIT_FAILURE;
    }

    auto group = perf::EventGroup({{PERF_TYPE_HW_CACHE, PERF_COUNT_HW_CACHE_LL | (PERF_COUNT_HW_CACHE_OP_READ << 8)
                                                            | (PERF_COUNT_HW_CACHE_RESULT_MISS << 16)},
                                   {PERF_TYPE_HW_CACHE, PERF_COUNT_HW_CACHE_LL | (PERF_COUNT_HW_CACHE_OP_READ << 8)
                                                            | (PERF_COUNT_HW_CACHE_RESULT_ACCESS << 16)},
                                   {PERF_TYPE_HW_CACHE, PERF_COUNT_HW_CACHE_LL | (PERF_COUNT_HW_CACHE_OP_WRITE << 8)
                                                            | (PERF_COUNT_HW_CACHE_RESULT_MISS << 16)},
                                   {PERF_TYPE_HW_CACHE, PERF_COUNT_HW_CACHE_LL | (PERF_COUNT_HW_CACHE_OP_WRITE << 8)
                                                            | (PERF_COUNT_HW_CACHE_RESULT_ACCESS << 16)}});

    // Note: This should be greater than the L3 cache size
    // memory = std::make_unique<std::vector<std::uint8_t>>(1'000'000'000);
    // for (int i = 0; i < 1'000'000'000; ++i) {
    //     memory->at(i) = i;
    // }

    group.reset();
    group.enable();

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

    group.disable();
    const auto counts = group.read();
    std::cout << "llc-read-misses    : " << counts[0] << std::endl;
    std::cout << "llc-read-accesses  : " << counts[1] << std::endl;
    std::cout << "llc-write-misses   : " << counts[2] << std::endl;
    std::cout << "llc-write-accesses : " << counts[3] << std::endl;
    std::cout << "llc-read-miss-rate : " << 100 * static_cast<double>(counts[0]) / static_cast<double>(counts[1])
              << std::endl;
    std::cout << "llc-write-miss-rate: " << 100 * static_cast<double>(counts[2]) / static_cast<double>(counts[3])
              << std::endl;
}
