#include <cstdio>
#include <cstdlib>

#include <dirent.h>
#include <sys/types.h>
#include <sys/wait.h>
#include <unistd.h>

#include <fmt/core.h>

void kill_process_tree(pid_t pid) {
    auto* dir = opendir(fmt::format("/proc/{}/task", pid).c_str());
    if (!dir) {
        fmt::println(stderr, "Failed to open /proc directory.");
        return;
    }

    struct dirent* entry;
    while ((entry = readdir(dir)) != nullptr) {
        if (entry->d_type == DT_DIR) {
            const auto tid = std::atoi(entry->d_name);
            if (tid <= 0 || tid == pid) {
                continue;
            }

            const auto path = fmt::format("/proc/{}/task/{}", pid, tid);
            if (auto* file = fopen(path.c_str(), "r")) {
                pid_t child_pid;
                while (fscanf(file, "%d", &child_pid) != EOF) {
                    kill_process_tree(child_pid);
                    kill(child_pid, SIGKILL);
                }

                fclose(file);
            }
        }
    }

    closedir(dir);

    kill(pid, SIGKILL);
}

int main(int argc, char** argv) {
    // First argument is delay in seconds, remaining arguments are the command to run.
    if (argc < 3) {
        fmt::println(stderr, "Usage: {} <delay> <command...>", argv[0]);
        return EXIT_FAILURE;
    }

    const auto delay_seconds = std::atoi(argv[1]);

    const pid_t pid = fork();
    if (pid == -1) {
        fmt::println(stderr, "Failed to fork.");
        return EXIT_FAILURE;
    }

    if (pid == 0) {
        execvp(argv[2], argv + 2);
        fmt::println(stderr, "Failed to execute command.");
        return EXIT_FAILURE;
    }

    sleep(delay_seconds);

    // If process has already exited after delay, return failure.
    int status;
    if (waitpid(pid, &status, WNOHANG) != 0) {
        fmt::println(stderr, "Process exited before timeout.");
        return EXIT_FAILURE;
    }

    // Kill the process and its descendants
    kill_process_tree(pid);
    waitpid(pid, &status, 0);
    if (!WIFSIGNALED(status) || WTERMSIG(status) != SIGKILL) {
        fmt::println(stderr, "Failed to kill process.");
        return EXIT_FAILURE;
    }

    return EXIT_SUCCESS;
}
