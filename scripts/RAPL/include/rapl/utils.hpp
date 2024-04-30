#pragma once

#include <chrono>
#include <condition_variable>
#include <functional>
#include <mutex>

struct KillableTimer {
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

struct ScopeExit {
    ScopeExit(std::function<void()> f) : f(std::move(f)) {}
    ~ScopeExit() {
        f();
    }
    std::function<void()> f;
};
;
