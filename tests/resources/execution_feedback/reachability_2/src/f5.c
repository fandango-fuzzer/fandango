#include "f.h"

void f5(char* buffer) {
    if (*buffer == '5'){
        f6(++buffer);
    }
}