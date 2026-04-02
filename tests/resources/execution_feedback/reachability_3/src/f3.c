#include "f.h"

void f3(char* buffer) {
    if (*buffer == '3'){
        f4(++buffer);
    }
}