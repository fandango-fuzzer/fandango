
# Base image
FROM ubuntu:24.04

# Install dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    git \
    libwrap0-dev \
    libssl-dev \
    libcrypt-dev \
    pkg-config \
    gcovr \
    lcov

RUN git clone https://github.com/djarosz/vsftpd.git

WORKDIR /vsftpd

#RUN make CFLAGS="-O2 -w" LIBS="-lssl -lcrypto -lcrypt -lwrap -lgcov"
RUN make CFLAGS="-O2 -w -fprofile-arcs -ftest-coverage" LIBS="-lssl -lcrypto -lcrypt -lwrap -lgcov"

# Create FTP users
RUN mkdir -p /home/the_user && chmod 750 /home/the_user
RUN groupadd the_user || true && \
    useradd -d /home/the_user -s /usr/sbin/nologin -g the_user the_user && \
    echo "the_user:the_password" | chpasswd && \
    chown the_user:the_user /home/the_user
RUN echo "root:the_password" | chpasswd
RUN grep -qxF '/usr/sbin/nologin' /etc/shells || echo '/usr/sbin/nologin' >> /etc/shells

# Copy vsftpd configuration
RUN mkdir -p /etc/vsftpd /var/run/vsftpd
COPY image/vsftpd.conf /etc/vsftpd/vsftpd.conf

RUN mkdir -p /usr/share/empty && \
    chmod 755 /usr/share/empty

# Expose FTP ports
ENV MIN_PORT=50000
ENV MAX_PORT=50100
EXPOSE 21
EXPOSE 50000-50100

# Start vsftpd
CMD ["./vsftpd", "/etc/vsftpd/vsftpd.conf"]
