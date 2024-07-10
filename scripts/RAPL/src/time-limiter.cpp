#include <cstdlib>
#include <iostream>
#include <vector>

#include <dirent.h>
#include <sys/types.h>
#include <sys/wait.h>
#include <unistd.h>

std::vector<pid_t> get_child_processes(pid_t pid) {
    std::vector<pid_t> children;

    auto* dir = opendir("/proc");
    if (!dir) {
        std::cerr << "Failed to open /proc directory." << std::endl;
        return {};
    }

    struct dirent* entry;
    while ((entry = readdir(dir)) != nullptr) {
        if (entry->d_type == DT_DIR) {
            const auto child_pid = pid_t(std::atoi(entry->d_name));
            if (child_pid <= 0 || child_pid == pid) {
                continue;
            }

            const auto path = std::string("/proc/") + entry->d_name + "/stat";
            if (auto* file = fopen(path.c_str(), "r")) {
                pid_t ppid;
                if (fscanf(file, "%*d %*s %*c %d", &ppid) != 1) {
                    std::cerr << "Failed to read parent PID from " << path << std::endl;
                    fclose(file);
                    continue;
                }
                fclose(file);

                if (ppid == pid) {
                    children.push_back(child_pid);
                    const auto subchildren = get_child_processes(child_pid);
                    children.insert(children.end(), subchildren.begin(), subchildren.end());
                }
            }
        }
    }

    closedir(dir);

    return children;
}

void kill_process_tree(pid_t pid) {
    std::vector<pid_t> children = get_child_processes(pid);

    // Kill all child processes.
    for (pid_t child_pid : children) {
        kill(child_pid, SIGKILL);
    }

    // Kill the original process.
    kill(pid, SIGKILL);
}

int main(int argc, char** argv) {
    // First argument is delay in seconds, remaining arguments are the command to run.
    if (argc < 3) {
        std::cerr << "Usage: " << argv[0] << " <delay> <command...>" << std::endl;
        return EXIT_FAILURE;
    }

    const auto delay_seconds = std::atoi(argv[1]);

    const pid_t pid = fork();
    if (pid == -1) {
        std::cerr << "Failed to fork." << std::endl;
        return EXIT_FAILURE;
    }

    if (pid == 0) {
        execvp(argv[2], argv + 2);
        std::cerr << "Failed to execute command." << std::endl;
        return EXIT_FAILURE;
    }

    sleep(delay_seconds);

    // If process has already exited after delay, return failure.
    int status;
    if (waitpid(pid, &status, WNOHANG) != 0) {
        return EXIT_FAILURE;
    }

    // Kill the process and its descendants
    kill_process_tree(pid);
    waitpid(pid, &status, 0);
    if (!WIFSIGNALED(status) || WTERMSIG(status) != SIGKILL) {
        std::cerr << "Failed to kill process." << std::endl;
        return EXIT_FAILURE;
    }

    return EXIT_SUCCESS;
}
