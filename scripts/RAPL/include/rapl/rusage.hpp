#pragma once

#include <sys/resource.h>
#include <sys/time.h>

#include <glaze/core/common.hpp>

struct timeval& operator-=(struct timeval& left, const struct timeval& right);
struct timeval operator-(struct timeval left, const struct timeval& right);

struct rusage& operator-=(struct rusage& left, const struct rusage& right);
struct rusage operator-(struct rusage left, const struct rusage& right);

template <>
struct glz::meta<struct timeval> {
    using T = struct timeval;
    [[maybe_unused]] static constexpr auto value = glz::object("tv_sec", &T::tv_sec, "tv_usec", &T::tv_usec);
};

template <>
struct glz::meta<struct rusage> {
    using T = struct rusage;
    // clang-format off
    [[maybe_unused]] static constexpr auto value = glz::object(
            "ru_utime", &T::ru_utime,
            "ru_stime", &T::ru_stime,
            "ru_maxrss", &T::ru_maxrss,
            "ru_ixrss", &T::ru_ixrss,
            "ru_idrss", &T::ru_idrss,
            "ru_isrss", &T::ru_isrss,
            "ru_minflt", &T::ru_minflt,
            "ru_majflt", &T::ru_majflt,
            "ru_nswap", &T::ru_nswap,
            "ru_inblock", &T::ru_inblock,
            "ru_oublock", &T::ru_oublock,
            "ru_msgsnd", &T::ru_msgsnd,
            "ru_msgrcv", &T::ru_msgrcv,
            "ru_nsignals", &T::ru_nsignals,
            "ru_nvcsw", &T::ru_nvcsw,
            "ru_nivcsw", &T::ru_nivcsw
    );
    // clang-format on
};
