#include <fcntl.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>

int my_func(const uint8_t *data, size_t size)
{
    if (size > 3 && data[0] == 'a' && data[1] == 'b' && data[2] == 'c')
    {
        // This will crash the fuzzer
        // complicated enough to prevent the compiler from complaining
        int *a = (int *)10;
        a -= 10;
        *a = 0;
    }

    return 0;
}

#if defined(INPUT_LIBFUZZER)
// Main fuzzing function
int LLVMFuzzerTestOneInput(const uint8_t *data, size_t size)
{
    return my_func(data, size);
}
#elif defined(INPUT_STDIN)
int main(int argc, char **argv)
{
    // for simplicity's sake: assume input is <1024 bytes long
    char data[1024];
    size_t n = fread(data, 1, sizeof(data), stdin);
    return my_func((uint8_t *)data, n);
}
#elif defined(INPUT_FILE)
int main(int argc, char **argv)
{
    uint8_t *data;
    size_t size;
    // Read from file
    FILE *f = fopen(argv[1], "rb");
    fseek(f, 0, SEEK_END);
    size = ftell(f);
    fseek(f, 0, SEEK_SET);
    data = malloc(size);
    fread(data, 1, size, f);
    fclose(f);
    my_func(data, size);
    free(data);
    return 0;
}
#else
int main(int argc, char **argv)
{
    return my_func((uint8_t *)argv[1], strlen(argv[1]));
}
#endif
