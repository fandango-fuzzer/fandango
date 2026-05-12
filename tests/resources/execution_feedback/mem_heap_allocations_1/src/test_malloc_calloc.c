#include <stdio.h>
#include <stdlib.h>

int main() {
    printf("yolo\n");
    for (int i = 0; i < 100; i++) {
        malloc(i);
    }

    for (int i = 0; i < 100; i++) {
        calloc(2, i);
    }
}   