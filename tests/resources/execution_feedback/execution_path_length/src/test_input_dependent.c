#include <stdio.h>
#include <stdlib.h>

int main(int argc, char* argv[]) {
    if (argc != 2) {
        printf("Usage: %s <file_with_input>\n", argv[0]);
        return 1;
    }

    FILE* file = fopen(argv[1], "r");
    if (file == NULL) {
        printf("Error: Could not open file %s\n", argv[1]);
        return 1;
    }

    char buffer[1000];
    if (fgets(buffer, sizeof(buffer), file) == NULL) {
        printf("Error: Could not read from file %s\n", argv[1]);
        fclose(file);
        return 1;
    }
    fclose(file);


    char* p = buffer;
    while (*p) {
        if (*p >= 0x30 && *p <= 0x39) {
            int iterations = *p - 0x30;
            for (int i = 0; i < iterations; i++) {
                printf(".");
            }
        }
        p++;
    }
    return 0;
}   