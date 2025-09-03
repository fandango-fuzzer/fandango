# Base image
FROM ubuntu:24.04

# Install dependencies
RUN apt-get update && apt-get install -y \
    clang \
    llvm \
    lcov \
    build-essential \
    git \
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
RUN cd /app && make clean && make

# Coverage folder
RUN mkdir -p /app/coverage_snapshots/gcda && chmod -R 777 /app/coverage_snapshots/gcda
RUN mkdir -p /usr/share/empty && chmod 755 /usr/share/empty

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

# Expose FTP ports
ENV MIN_PORT=50000
ENV MAX_PORT=50100
EXPOSE 21
EXPOSE 50000-50100

# Coverage snapshot script
COPY image/coverage_snapshots_loop.sh .

VOLUME /app/coverage_snapshots

# Run vsftpd and coverage loop
CMD ["bash", "coverage_snapshots_loop.sh"]