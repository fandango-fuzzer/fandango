#include <signal.h>
#include <unistd.h>

__attribute__((weak)) void __gcov_dump(void);

static void
fandango_gcov_dump_handler(int signum) {
	if (__gcov_dump != 0) {
		__gcov_dump();
	}
	signal(signum, SIG_DFL);
	raise(signum);
}

__attribute__((constructor)) static void
fandango_gcov_install_handlers(void) {
	signal(SIGTERM, fandango_gcov_dump_handler);
	signal(SIGINT, fandango_gcov_dump_handler);
}
/* ----------------------------------------------------------------------- */
