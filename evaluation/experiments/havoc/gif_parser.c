#include <stdio.h>
#include <unistd.h>
#include "giflib-code/gif_lib.h"

int main(int argc, char *argv[])
{
    int error = 0;
    GifFileType *gif = DGifOpenFileHandle(STDIN_FILENO, &error);

    if (gif == NULL)
        return 1;

    DGifSlurp(gif);
    DGifCloseFile(gif, &error);
    return 0;
}