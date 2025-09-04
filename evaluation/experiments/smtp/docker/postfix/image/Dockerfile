# Use Ubuntu as base
FROM ubuntu:22.04

# Install dependencies
RUN apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y \
    build-essential clang bison flex libssl-dev libsasl2-dev \
    libdb-dev libldap2-dev zlib1g-dev curl wget git sasl2-bin

# Set working directory
WORKDIR /src

# Download Postfix source
RUN wget https://de.postfix.org/ftpmirror/official/postfix-3.8.11.tar.gz && \
    tar xvf postfix-3.8.11.tar.gz && rm postfix-3.8.11.tar.gz

WORKDIR /src/postfix-3.8.11

# Create minimal Postfix config files
RUN mkdir -p /etc/postfix && \
    echo "myhostname = localhost" > /etc/postfix/main.cf && \
    echo "mydomain = localdomain" >> /etc/postfix/main.cf && \
    echo "myorigin = /etc/mailname" >> /etc/postfix/main.cf && \
    echo "smtpd_sasl_auth_enable = yes" >> /etc/postfix/main.cf && \
    echo "smtpd_sasl_type = cyrus" >> /etc/postfix/main.cf && \
    echo "smtpd_sasl_path = smtpd" >> /etc/postfix/main.cf && \
    echo "smtpd_sasl_local_domain =" >> /etc/postfix/main.cf && \
    echo "smtpd_recipient_restrictions = permit_sasl_authenticated, reject" >> /etc/postfix/main.cf && \
    echo "inet_interfaces = all" >> /etc/postfix/main.cf && \
    echo "inet_protocols = ipv4" >> /etc/postfix/main.cf
RUN echo "smtp      inet  n       -       y       -       -       smtpd" > /etc/postfix/master.cf

# Coverage build
#ENV CFLAGS="-O1 -g -fsanitize=address,fuzzer-coverage=1"
#ENV CXXFLAGS="-O1 -g -fsanitize=address,fuzzer-coverage=1"

# Build
RUN make
RUN make postfix-install -non-interactive
#RUN make -f Makefile.init makefiles && make

# Install Postfix (creates /usr/local/libexec/postfix/postfix)
#RUN make -f Makefile.init install

# Verify binaries
#RUN ls -l /usr/local/libexec/postfix/

# Create directories for logs and coverage
#RUN mkdir -p /var/spool/postfix /var/log/postfix /coverage

# Add SASL user
RUN echo "the_password" | saslpasswd2 -p -c the_user && \
    chown root:root /etc/sasldb2 && chmod 600 /etc/sasldb2

# Expose SMTP port
EXPOSE 25

CMD ["./postfix", "start"]

# Start Postfix from installed libexec path
# CMD ["sh", "-c", "ASAN_OPTIONS=coverage_dir=/coverage:detect_leaks=0 /usr/local/lib/postfix/postfix start-fg"]