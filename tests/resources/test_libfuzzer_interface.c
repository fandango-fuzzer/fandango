#include <stdio.h>

int LLVMFuzzerTestOneInput(const unsigned char *data, size_t size) {
    printf("data: %s\n", (char *)data);
    return 0;
}