extern void __gcov_dump(void) __attribute__((weak));

static void
smtpd_gcov_set_prefix(void)
{
	char prefix[256];
	char tmp[32];
	int n, t, p, i;
	pid_t pid;

	/* Build "/home/ubuntu/cov_raw/<pid>" */
	pid = getpid();
	t = 0;
	if (pid <= 0) {
		tmp[t++] = '0';
	} else {
		while (pid > 0 && t < (int)sizeof(tmp)) {
			tmp[t++] = (char)('0' + (pid % 10));
			pid /= 10;
		}
	}

	{
		const char *base = "/cov_raw/";
		p = 0;
		for (i = 0; base[i] != '\0' && p < (int)sizeof(prefix) - 1; i++)
			prefix[p++] = base[i];
		for (n = t; n > 0 && p < (int)sizeof(prefix) - 1; n--)
			prefix[p++] = tmp[n - 1];
		prefix[p] = '\0';
	}

	setenv("GCOV_PREFIX", prefix, 1);
}

static void
smtpd_gcov_flush_handler(int sig)
{
	(void)sig;
	if (__gcov_dump)
		__gcov_dump();
	_exit(0);
}

static void __attribute__((constructor(101)))
smtpd_gcov_install(void)
{
	struct sigaction sa;

	smtpd_gcov_set_prefix();

	memset(&sa, 0, sizeof(sa));
	sa.sa_handler = smtpd_gcov_flush_handler;
	sigaction(SIGUSR1, &sa, NULL);
}
