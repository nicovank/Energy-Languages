cmake_minimum_required(VERSION 3.19)

include(FetchContent)
include(CheckIPOSupported)

project(RAPL)

set(CMAKE_CXX_STANDARD 20)

find_package(Threads REQUIRED)

FetchContent_Declare(
  argparse
  GIT_REPOSITORY https://github.com/p-ranav/argparse.git
  GIT_TAG af442b4da0cd7a07b56fa709bd16571889dc7fda # v3.0
)

FetchContent_Declare(
  benchmark
  GIT_REPOSITORY https://github.com/google/benchmark.git
  GIT_TAG 344117638c8ff7e239044fd0fa7085839fc03021 # v1.8.3
)

FetchContent_Declare(
  fmt
  GIT_REPOSITORY https://github.com/fmtlib/fmt.git
  GIT_TAG e69e5f977d458f2650bb346dadf2ad30c5320281 # 10.2.1
)

FetchContent_Declare(
    glaze
    GIT_REPOSITORY https://github.com/stephenberry/glaze.git
    GIT_TAG cc58afa1f751513daa482a905e6021f5dcc5fe2c # v2.4.4
)

message(STATUS "Downloading and configuring argparse")
FetchContent_MakeAvailable(argparse)

message(STATUS "Downloading and configuring Benchmark")
set(BENCHMARK_ENABLE_TESTING OFF)
FetchContent_MakeAvailable(benchmark)

message(STATUS "Downloading and configuring {fmt}")
FetchContent_MakeAvailable(fmt)

message(STATUS "Downloading and configuring Glaze")
FetchContent_MakeAvailable(glaze)

check_ipo_supported(RESULT IPO_SUPPORTED)
if(IPO_SUPPORTED)
    message(STATUS "Enabling IPO/LTO")
    set(CMAKE_INTERPROCEDURAL_OPTIMIZATION ON)
else()
    message(STATUS "IPO/LTO is not supported")
endif()

add_library(rapl_lib STATIC src/cpu.cpp src/msr.cpp src/perf.cpp src/rapl.cpp src/rusage.cpp)
target_compile_options(rapl_lib PRIVATE -Wall -Wextra -Wpedantic -Werror)
target_include_directories(rapl_lib PUBLIC include)
target_link_libraries(rapl_lib PRIVATE glaze::glaze)
target_link_libraries(rapl_lib PRIVATE m)
target_link_libraries(rapl_lib PRIVATE Threads::Threads)

include(${CMAKE_SOURCE_DIR}/cmake/checkRaplSupport.cmake)
if(RAPL_MSR_PKG_SUPPORTED)
    target_compile_options(rapl_lib PUBLIC -DRAPL_MSR_PKG_SUPPORTED)
endif()
if(RAPL_MSR_PP0_SUPPORTED)
    target_compile_options(rapl_lib PUBLIC -DRAPL_MSR_PP0_SUPPORTED)
endif()
if(RAPL_MSR_PP1_SUPPORTED)
    target_compile_options(rapl_lib PUBLIC -DRAPL_MSR_PP1_SUPPORTED)
endif()
if(RAPL_MSR_DRAM_SUPPORTED)
    target_compile_options(rapl_lib PUBLIC -DRAPL_MSR_DRAM_SUPPORTED)
endif()

add_executable(rapl src/main.cpp)
target_compile_options(rapl PRIVATE -Wall -Wextra -Wpedantic -Werror)
target_link_libraries(rapl PRIVATE argparse)
target_link_libraries(rapl PRIVATE glaze::glaze)
target_link_libraries(rapl PRIVATE rapl_lib)

add_executable(time-limiter src/time-limiter.cpp)
target_compile_options(time-limiter PRIVATE -Wall -Wextra -Wpedantic -Werror)

add_executable(benchmark_iteration src/benchmarks/iteration.cpp)
target_compile_options(benchmark_iteration PRIVATE -Wall -Wextra -Wpedantic -Werror)
target_link_libraries(benchmark_iteration PRIVATE argparse)
target_link_libraries(benchmark_iteration PRIVATE benchmark)
target_link_libraries(benchmark_iteration PRIVATE glaze::glaze)
target_link_libraries(benchmark_iteration PRIVATE rapl_lib)
target_link_libraries(benchmark_iteration PRIVATE Threads::Threads)

add_executable(benchmark_prediction src/benchmarks/prediction.cpp)
target_compile_options(benchmark_prediction PRIVATE -Wall -Wextra -Wpedantic -Werror)
target_link_libraries(benchmark_prediction PRIVATE argparse)
target_link_libraries(benchmark_prediction PRIVATE benchmark)
target_link_libraries(benchmark_prediction PRIVATE glaze::glaze)
target_link_libraries(benchmark_prediction PRIVATE rapl_lib)
