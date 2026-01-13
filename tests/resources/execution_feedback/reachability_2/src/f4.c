#include "f.h"

void f4(char* buffer) {
    if (*buffer == '4'){
        f5(++buffer);
    }
}