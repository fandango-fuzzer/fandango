#include "f.h"

void f9(char* buffer) {
    printf("f9 found!\n");
    if (*buffer++ == '9') {
        if (*buffer++ == '0') {
            if (*buffer == '0'){
                // solution: 0012345678900...
                printf("needle found!\n");
            }
        }
    }
}