# Use an Ubuntu base image
FROM ubuntu:24.04

# Install dependencies
RUN apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y \
    build-essential \
    gcc \
    nano \
    g++ \
    make \
    stunnel4 \
    wget \
    git \
    pkg-config \
    libssl-dev \
    libevent-dev \
    bison \
    libtool \
    sudo \
    zip \
    zlib1g-dev \
    ca-certificates \
    swaks \
    locales && \
    locale-gen en_US.UTF-8 && \
    rm -rf /var/lib/apt/lists/*

# Create a non-root user
RUN useradd -ms /bin/bash the_user && echo "the_user:the_password" | chpasswd && adduser the_user sudo

# Set environment variables for coverage compilation
ENV CFLAGS="-fprofile-arcs -ftest-coverage -O0"
ENV CXXFLAGS="-fprofile-arcs -ftest-coverage -O0"
ENV LDFLAGS="--coverage"

WORKDIR /home/app

# Download and prepare OpenSMTPD source
RUN wget https://github.com/OpenSMTPD/OpenSMTPD/archive/refs/tags/7.7.0p0.zip && \
    unzip 7.7.0p0.zip && \
    rm 7.7.0p0.zip

WORKDIR /home/app/OpenSMTPD-7.7.0p0

# Delete both lines that enforce TLS requirement for auth
#RUN sed -i '/if (lo->auth != 0 && !lo->ssl)/,+1d' usr.sbin/smtpd/parse.y
# Patch parse.y to force AUTH on plaintext listeners
#RUN sed -i 's/^\([[:space:]]*\)flags = lo->flags;/\1if (lo->auth == 0) lo->auth = F_AUTH;\n\1lo->flags |= lo->auth;\n\1flags = lo->flags;/' usr.sbin/smtpd/parse.y
# Build OpenSMTPD with coverage
RUN ./bootstrap && \
    ./configure --disable-portable --enable-plaintext-auth && \
    make && make install

RUN mkdir -p /etc/smtpd
COPY smtpd.conf /etc/
COPY credentials /etc/smtpd/

RUN mkdir -p /etc/ssl/private && \
    openssl req -x509 -nodes -days 365 -newkey rsa:2048 \
        -keyout /etc/ssl/private/server.key \
        -out /etc/ssl/certs/server.crt \
        -subj "/CN=localhost"

RUN mkdir -p /etc/stunnel
COPY stunnel.conf /etc/stunnel

# Add system users
RUN mkdir /var/empty && \
    useradd -c "SMTP Daemon" -d /var/empty -s /sbin/nologin _smtpd &&\
    useradd -c "SMTPD Queue" -d /var/empty -s /sbin/nologin _smtpq

RUN mkdir -p /var/spool/smtpd/data

RUN chown 0:0 /var/spool/smtpd && \
    chmod 711 /var/spool/smtpd

RUN mkdir -p /var/spool/smtpd/queue && \
    chown _smtpq:0 /var/spool/smtpd/queue && \
    chmod 700 /var/spool/smtpd/queue

RUN mkdir -p /var/spool/smtpd/control && \
    chown _smtpd:_smtpd /var/spool/smtpd/control && \
    chmod 711 /var/spool/smtpd/control

RUN mkdir -p /var/run/smtpd && \
    chown _smtpd /var/run/smtpd

RUN mkdir -p /var/lib/ssl/certs && \
    cp -r /etc/ssl/certs/* /var/lib/ssl/certs

RUN mkdir -p /var/mail

RUN mkdir -p /var/run/smtpd/ca /var/run/smtpd/dispatcher /var/run/smtpd/scheduler /var/run/smtpd/control /var/run/smtpd/queue && \
    chown _smtpd:_smtpd /var/run/smtpd/* && chmod 755 /var/run/smtpd/*

RUN mkdir -p /var/mail && \
    chown the_user:the_user /var/mail && \
    touch /var/mail/the_user && \
    chown the_user:the_user /var/mail/the_user


# Default command
CMD smtpd -d -F -f /etc/smtpd.conf & stunnel /etc/stunnel/stunnel.conf