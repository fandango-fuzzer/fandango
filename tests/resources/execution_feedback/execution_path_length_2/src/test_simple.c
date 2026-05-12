#include <stdio.h>

int main(int argc, char* argv[]) {
    for (int i = 0; i < 100; i++) {
        printf(".");
    }

    for (int i = 0; i < 100; i++) {
         printf(",");
    }

    if (argc==2) {
        return 0;
    }
    return 1;
}