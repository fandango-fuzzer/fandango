#include "f.h"

void f1(char* buffer) {
    if (*buffer++ == '0') {
        if (*buffer++ == '0') {
            if (*buffer == '1'){
                f2(++buffer);
            }
        }
    }
}