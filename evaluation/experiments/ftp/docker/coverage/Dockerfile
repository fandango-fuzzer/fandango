# Base image
FROM ubuntu:24.04

# Install dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    git \
    lcov \
    python3 \
    python3-pip \
    g++ \
    make \
    wget \
    passwd \
    libwrap0-dev \
    libssl-dev \
    && rm -rf /var/lib/apt/lists/*

# Python dependencies for plotting
RUN pip3 install --break-system-packages pandas matplotlib

# Set working directory
WORKDIR /app

# Clone project
RUN git clone https://github.com/djarosz/vsftpd.git /app
COPY image/Makefile /app/Makefile

# Build vsftpd with coverage flags (use CFLAGS, not CXXFLAGS)
RUN cd /app && make clean && make

# ------------------------------
# Hardcode FTP user and folder
# ------------------------------

# FTP server config folder
RUN mkdir -p /etc/vsftpd && mkdir -p /var/run/vsftpd

# Copy vsftpd configuration
COPY image/vsftpd.conf /etc/vsftpd/vsftpd.conf
ENV PATH="/app:${PATH}"

RUN mkdir -p /usr/share/empty
RUN mkdir -p /usr/share/empty && chmod 755 /usr/share/empty

# Create home folder and user
RUN mkdir -p /home/the_user && chmod 750 /home/the_user
RUN groupadd the_user || true && \
    useradd -d /home/the_user -s /usr/sbin/nologin -g the_user the_user && \
    echo "the_user:the_password" | chpasswd && \
    mkdir -p /home/the_user
RUN chown the_user:the_user /home/the_user
RUN chmod 750 /home/the_user

RUN grep -qxF '/usr/sbin/nologin' /etc/shells || echo '/usr/sbin/nologin' >> /etc/shells
RUN mkdir -p /app/coverage_snapshots/gcda \
    && chown -R the_user:the_user /app/coverage_snapshots/gcda

# Hardcode FTP server ports
ENV MIN_PORT=50000
ENV MAX_PORT=50100

# Expose FTP port and passive range
EXPOSE 21
EXPOSE 50000-50100

# ------------------------------
# Coverage snapshot script
# ------------------------------
COPY image/coverage_snapshots_loop.sh .

VOLUME /app/coverage_snapshots

# Run vsftpd and coverage loop by default
CMD ["bash", "coverage_snapshots_loop.sh"]