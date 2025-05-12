#include <fcntl.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>

// Compile-time options for input method:
// #define USE_STDIN    // Read from stdin
// #define USE_ARG      // Use first argument directly
// #define USE_FILE     // Read from file specified in first argument

void crash()
{
    // This will crash the fuzzer
    // complicated enough to prevent the compiler from complaining
    int *a = (int *)10;
    a -= 10;
    *a = 0;
}

// Main fuzzing function
int LLVMFuzzerTestOneInput(const uint8_t *data, size_t size)
{
    if (size > 3 && data[0] == 'a' && data[1] == 'b' && data[2] == 'c')
        crash();

    return 0;
}

#ifndef LIBFUZZER

int main(int argc, char **argv)
{
    uint8_t *data;
    size_t size;
#if defined(INPUT_STDIN)
    // Read from stdin
    u_int8_t buffer[1024];
    ssize_t bytes_read = read(STDIN_FILENO, buffer, 1024);
    data = buffer;
    size = bytes_read;
#elif defined(INPUT_FILE)
    // Read from file
    FILE *f = fopen(argv[1], "rb");
    fseek(f, 0, SEEK_END);
    size = ftell(f);
    fseek(f, 0, SEEK_SET);
    data = malloc(size);
    fread(data, 1, size, f);
    fclose(f);
#else
    // Default to using argument directly
    data = (uint8_t *)argv[1];
    size = strlen(argv[1]);
#endif

    LLVMFuzzerTestOneInput(data, size);

#if defined(INPUT_FILE)
    free(data);
#endif

    return 0;
}

#endif
