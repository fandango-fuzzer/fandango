#include <signal.h>
#include <string.h>
#include <unistd.h>


extern void __gcov_dump(void) __attribute__((weak));

static void
fandango_gcov_dump_handler(int signum)
{
	if (__gcov_dump != 0)
		__gcov_dump();
	signal(signum, SIG_DFL);
	raise(signum);
}

static void __attribute__((constructor))
fandango_gcov_install(void)
{
	struct sigaction sa;

	memset(&sa, 0, sizeof(sa));
	sa.sa_handler = fandango_gcov_dump_handler;
	sigaction(SIGTERM, &sa, NULL);
	sigaction(SIGINT, &sa, NULL);
}
