FROM ubuntu:24.04

# Install dependencies
# Install dependencies (added autotools)
RUN apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y \
    build-essential \
    gcc \
    g++ \
    make \
    git \
    wget \
    pkg-config \
    autoconf \
    automake \
    libtool \
    libssl-dev \
    libuv1-dev \
    libnghttp2-dev \
    libprotobuf-c-dev \
    protobuf-c-compiler \
    zlib1g-dev \
    liburcu-dev \
    libcap-dev \
    libcmocka-dev \
    python3 \
    zip \
    python3-ply \
    python3-pip \
    lcov \
    dnsutils \
    sudo && \
    rm -rf /var/lib/apt/lists/*

# Add a non-root user for running bind
RUN useradd -ms /bin/bash binduser && echo "binduser:bindpass" | chpasswd

# Environment variables for coverage
ENV CFLAGS="-fprofile-arcs -ftest-coverage -O0"
ENV CXXFLAGS="-fprofile-arcs -ftest-coverage -O0"
ENV LDFLAGS="--coverage"

# Download Bind9 source (example: 9.18 branch)
WORKDIR /home/binduser
RUN wget https://gitlab.isc.org/isc-projects/bind9/-/archive/stable/bind9-stable.zip?ref_type=tags -O bind9-stable.zip
RUN unzip bind9-stable.zip && mv bind9-stable bind9 && rm bind9-stable.zip

WORKDIR /home/binduser/bind9
RUN autoreconf -fi
RUN ./configure --prefix=/home/binduser/.local --with-openssl --enable-developer && \
    make -j$(nproc) && \
    make install

# Create config directory
RUN mkdir -p /etc/bind/zones

# Minimal named.conf to start
COPY named.conf /etc/bind/named.conf
COPY zones/* /etc/bind/zones/

# Create runtime directories and fix permissions
RUN mkdir -p /var/cache/bind /var/run/named /var/log/named

COPY coverage_loop.sh /usr/local/bin/
RUN chmod +x /usr/local/bin/coverage_loop.sh
RUN mkdir -p /home/binduser/coverage/

# Expose DNS ports
EXPOSE 53/udp
EXPOSE 53/tcp


# Default command: start bind9 in foreground
# Wrapper to run named and coverage in background
CMD ["/bin/bash", "-c", "\
/usr/local/bin/coverage_loop.sh & \
exec /home/binduser/.local/sbin/named -c /etc/bind/named.conf -f -g \
"]