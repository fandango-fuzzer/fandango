#!/bin/bash

# Coverage folder must exist and be writable BEFORE vsftpd starts
GCOV_DIR=/app/coverage_snapshots/gcda
mkdir -p "$GCOV_DIR"
chown -R the_user:the_user "$GCOV_DIR"
chmod 777 "$GCOV_DIR"   # optional, just in case

export GCOV_PREFIX="$GCOV_DIR"
export GCOV_PREFIX_STRIP=1

mkdir -p coverage_snapshots
CSV_FILE=coverage_snapshots/summary.csv
[ ! -f "$CSV_FILE" ] && echo "timestamp,coverage" > "$CSV_FILE"

# Start vsftpd in background
/app/vsftpd /etc/vsftpd/vsftpd.conf &
VSFTPD_PID=$!

# Loop to capture coverage
BUILD_DIR=/app
while true; do
    TIMESTAMP=$(date +%s)
    lcov --capture --directory "$BUILD_DIR" --output-file coverage_$TIMESTAMP.info
    lcov --remove coverage_$TIMESTAMP.info '/usr/*' --output-file coverage_$TIMESTAMP.info
    COVERAGE=$(lcov --summary coverage_$TIMESTAMP.info | grep 'lines' | awk '{print $2}' | tr -d '%')
    echo "$TIMESTAMP,$COVERAGE" >> $CSV_FILE
    sleep 5
done

trap "kill $VSFTPD_PID" EXIT