#include <string.h>

#include "f.h"

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

    // char* buffer = argv[1];
    if (strlen(buffer) < 13) {
        printf("Error: <string> must be at least 13 characters long.\n");
        return 1;
    }

    f1(buffer);
    return 0;
}