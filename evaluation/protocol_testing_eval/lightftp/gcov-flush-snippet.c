#include <signal.h>
#include <unistd.h>

extern void __gcov_dump(void);

static void _fandango_sigusr1(int signo) { (void)signo; __gcov_dump(); _exit(0); }

__attribute__((constructor)) static void _fandango_gcov_setup(void) { signal(SIGUSR1, _fandango_sigusr1); }
