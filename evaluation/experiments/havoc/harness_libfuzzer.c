#include "giflib-code-libfuzzer/gif_lib.h"
#include <fcntl.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/mman.h>
#include <sys/stat.h>
#include <unistd.h>

void crash(const char *message)
{
    printf("Crash: %s\n", message);
    FILE *fp = fopen("harness-crashes.log", "a+");
    if (fp != NULL)
    {
        fprintf(fp, "%s\n", message);
        fclose(fp);
    }
    int *a = (int *)10;
    a -= 10;
    *a = 0;
}

// Structure to hold our buffer information
typedef struct
{
    const uint8_t *data;
    size_t size;
    size_t pos;
} BufferInfo;

// Custom read function that reads from our buffer
static int readFromBuffer(GifFileType *gif, GifByteType *buf, int len)
{
    BufferInfo *info = (BufferInfo *)gif->UserData;
    if (info->pos >= info->size)
        return 0;

    int to_read = len;
    if (info->pos + to_read > info->size)
    {
        to_read = info->size - info->pos;
    }

    memcpy(buf, info->data + info->pos, to_read);
    info->pos += to_read;
    return to_read;
}

// Main fuzzing function
int LLVMFuzzerTestOneInput(const uint8_t *data, size_t size)
{
    int error = 0;

    BufferInfo info = {.data = data, .size = size, .pos = 0};
    GifFileType *gif = DGifOpen(&info, readFromBuffer, &error);
    if (gif == NULL)
    {
        // ignore illegal gif files, it's a fuzzer!
        return 0;
    }

    DGifSlurp(gif);
    DGifCloseFile(gif, &error);
    return 0;
}
