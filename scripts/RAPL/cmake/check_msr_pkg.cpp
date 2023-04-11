#include <cstdint>
#include <fcntl.h>
#include <unistd.h>

#define MSR_PKG_ENERGY_STATUS 0x611

int main() {
    const auto fd = open("/dev/cpu/0/msr", O_RDONLY);
    if (fd == -1) {
        return 1;
    }

    int64_t data;
    if (pread(fd, &data, sizeof(int64_t), MSR_PKG_ENERGY_STATUS) != sizeof(int64_t)) {
        return 1;
    }

    close(fd);
}