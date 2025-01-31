cmake_minimum_required(VERSION 3.11)

include(FetchContent)

project(c-vs-numpy-matmul)

FetchContent_Declare(
  benchmark
  GIT_REPOSITORY https://github.com/google/benchmark.git
  GIT_TAG c58e6d0710581e3a08d65c349664128a8d9a2461 # v1.9.1
)

message(STATUS "Downloading and configuring Benchmark")
set(BENCHMARK_ENABLE_TESTING OFF)
FetchContent_MakeAvailable(benchmark)

add_executable(cpp-matmul matmul.cpp)
target_link_libraries(cpp-matmul benchmark::benchmark)
