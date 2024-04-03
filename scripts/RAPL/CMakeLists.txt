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
    GIT_TAG b99111789445dc3693c7542dabe1ee1538a39611 # v1.3.5
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

add_library(rapl_lib STATIC src/cpu.cpp src/msr.cpp src/perf.cpp src/rapl.cpp)
target_compile_options(rapl_lib PRIVATE -Wall -Wextra -Wpedantic -Werror)
target_include_directories(rapl_lib PUBLIC include)
target_link_libraries(rapl_lib PRIVATE m)

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
target_link_libraries(rapl PRIVATE rapl_lib)
target_link_libraries(rapl PRIVATE glaze::glaze)
target_link_libraries(rapl PRIVATE Threads::Threads)

add_executable(idle src/idle.cpp)
target_compile_options(idle PRIVATE -Wall -Wextra -Wpedantic -Werror)
target_link_libraries(idle PRIVATE rapl_lib)
target_link_libraries(idle PRIVATE Threads::Threads)

add_executable(benchmark_iteration src/benchmarks/iteration.cpp)
target_compile_options(benchmark_iteration PRIVATE -Wall -Wextra -Wpedantic -Werror)
target_link_libraries(benchmark_iteration PRIVATE argparse)
target_link_libraries(benchmark_iteration PRIVATE benchmark)
target_link_libraries(benchmark_iteration PRIVATE rapl_lib)
target_link_libraries(benchmark_iteration PRIVATE Threads::Threads)

add_executable(benchmark_prediction src/benchmarks/prediction.cpp)
target_compile_options(benchmark_prediction PRIVATE -Wall -Wextra -Wpedantic -Werror)
target_link_libraries(benchmark_prediction PRIVATE argparse)
target_link_libraries(benchmark_prediction PRIVATE benchmark)
target_link_libraries(benchmark_prediction PRIVATE fmt)
target_link_libraries(benchmark_prediction PRIVATE rapl_lib)

check_ipo_supported(RESULT IPO_SUPPORTED)
if(IPO_SUPPORTED)
    message(DEBUG "Enabling IPO/LTO")
    set_property(TARGET rapl_lib PROPERTY INTERPROCEDURAL_OPTIMIZATION TRUE)
    set_property(TARGET rapl PROPERTY INTERPROCEDURAL_OPTIMIZATION TRUE)
    set_property(TARGET idle PROPERTY INTERPROCEDURAL_OPTIMIZATION TRUE)
    set_property(TARGET benchmark_iteration PROPERTY INTERPROCEDURAL_OPTIMIZATION TRUE)
    set_property(TARGET benchmark_prediction PROPERTY INTERPROCEDURAL_OPTIMIZATION TRUE)
else()
    message(DEBUG "IPO/LTO is not supported")
endif()
