#include "f.h"

void f2(char* buffer) {
    if (*buffer == '2'){
        f3(++buffer);
    }
}