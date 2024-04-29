#include <rapl/rusage.hpp>

#include <type_traits>

struct timeval& operator-=(struct timeval& left, const struct timeval& right) {
    static_assert(std::is_signed_v<time_t>);
    left.tv_sec -= right.tv_sec;
    left.tv_usec -= right.tv_usec;
    if (left.tv_usec < 0) {
        left.tv_sec -= 1;
        left.tv_usec += 1000000;
    }
    return left;
}

struct timeval operator-(struct timeval left, const struct timeval& right) {
    left -= right;
    return left;
}

struct rusage& operator-=(struct rusage& left, const struct rusage& right) {
    left.ru_utime -= right.ru_utime;
    left.ru_stime -= right.ru_stime;
    left.ru_maxrss -= right.ru_maxrss;
    left.ru_ixrss -= right.ru_ixrss;
    left.ru_idrss -= right.ru_idrss;
    left.ru_isrss -= right.ru_isrss;
    left.ru_minflt -= right.ru_minflt;
    left.ru_majflt -= right.ru_majflt;
    left.ru_nswap -= right.ru_nswap;
    left.ru_inblock -= right.ru_inblock;
    left.ru_oublock -= right.ru_oublock;
    left.ru_msgsnd -= right.ru_msgsnd;
    left.ru_msgrcv -= right.ru_msgrcv;
    left.ru_nsignals -= right.ru_nsignals;
    left.ru_nvcsw -= right.ru_nvcsw;
    left.ru_nivcsw -= right.ru_nivcsw;

    return left;
}

struct rusage operator-(struct rusage left, const struct rusage& right) {
    left -= right;
    return left;
}
