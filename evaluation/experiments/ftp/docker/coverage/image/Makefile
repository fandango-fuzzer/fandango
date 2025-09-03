# Compiler
CC = clang

# Compiler flags
CFLAGS = -O0 -g -Wall -W -Wshadow -Wformat-security \
         -U_FORTIFY_SOURCE -D_FORTIFY_SOURCE=2 -DONE_PROCESS \
         -fprofile-instr-generate -fcoverage-mapping

IFLAGS = -idirafter dummyinc

# Linker flags
LDFLAGS = -fprofile-instr-generate -fcoverage-mapping -fPIE -pie

# Libraries
LIBS = `./vsf_findlibs.sh` -lcrypt -lssl -lcrypto

# Source files
SRCS = main.c utility.c prelogin.c ftpcmdio.c postlogin.c privsock.c \
       tunables.c ftpdataio.c secbuf.c ls.c \
       postprivparent.c logging.c str.c netstr.c sysstr.c strlist.c \
       banner.c filestr.c parseconf.c secutil.c \
       ascii.c oneprocess.c twoprocess.c privops.c standalone.c hash.c \
       tcpwrap.c ipaddrparse.c access.c features.c readwrite.c opts.c \
       ssl.c sslslave.c ptracesandbox.c ftppolicy.c sysutil.c sysdeputil.c \
       seccompsandbox.c

OBJS = $(SRCS:.c=.o)

# Build vsftpd binary
vsftpd: $(OBJS)
	$(CC) -o $@ $(OBJS) $(LDFLAGS) $(LIBS)

# Compile .c -> .o
%.o: %.c
	$(CC) -c $< $(CFLAGS) $(IFLAGS)

# Install binary
install:
	if [ -x /usr/local/sbin ]; then \
		install -m 755 vsftpd /usr/local/sbin/vsftpd; \
	else \
		install -m 755 vsftpd /usr/sbin/vsftpd; \
	fi

# Clean build
clean:
	rm -f $(OBJS) vsftpd *.gcno *.gcda *.profraw