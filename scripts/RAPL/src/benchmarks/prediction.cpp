#include <cstdint>
#include <deque>
#include <iostream>
#include <random>
#include <vector>

#include <argparse/argparse.hpp>
#include <benchmark/benchmark.h>

int main(int argc, char** argv) {
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
        .metavar("N")
        .scan<'g', double>();

    try {
        program.parse_args(argc, argv);
    } catch (const std::exception& err) {
        std::cerr << err.what() << std::endl;
        std::cerr << program;
        return EXIT_FAILURE;
    }

    const auto n = program.get<std::uint64_t>("n");
    const auto iterations = program.get<std::uint64_t>("iterations");
    const auto p = program.get<double>("p");

    auto generator = std::mt19937_64(std::random_device()());

    std::vector<std::uint64_t> a(n);
    std::generate(a.begin(), a.end(),
                  [&generator]() { return std::uniform_int_distribution<std::uint64_t>()(generator); });
    std::vector<std::uint64_t> b(n);
    std::generate(b.begin(), b.end(),
                  [&generator]() { return std::uniform_int_distribution<std::uint64_t>()(generator); });

    /* std::vector<bool> */ std::deque<bool> conditions(iterations);
    std::generate(conditions.begin(), conditions.end(),
                  [p, &generator]() { return std::bernoulli_distribution(p)(generator); });

    std::uint64_t sum = 0;
    for (std::uint64_t i = 0; i < iterations; ++i) {
        if (conditions[i]) {
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
