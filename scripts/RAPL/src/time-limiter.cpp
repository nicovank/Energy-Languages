#include <cstdlib>
#include <iostream>

#include <sys/types.h>
#include <sys/wait.h>
#include <unistd.h>

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

    // Kill the process and return success.
    kill(pid, SIGKILL);
    waitpid(pid, &status, 0);
    if (!WIFSIGNALED(status) || WTERMSIG(status) != SIGKILL) {
        std::cerr << "Failed to kill process." << std::endl;
        return EXIT_FAILURE;
    }

    return EXIT_SUCCESS;
}
