#!/bin/bash

CSV_FILE=coverage_snapshots/summary.csv
[ ! -f "$CSV_FILE" ] && echo "timestamp,coverage" > "$CSV_FILE"

# Start smtpd in background
smtpd -d -F -f /etc/smtpd.conf &
SMTPD_PID=$!

trap "kill $SMTPD_PID" EXIT

BUILD_DIR="usr.sbin/smtpd"
CSV_FILE="/app/coverage/coverage.csv"

while true; do
    TIMESTAMP=$(date +%s)
    #lcov --capture \
    #     --directory "$BUILD_DIR" \
    #     --output-file coverage_$TIMESTAMP.info
    #lcov --remove coverage_$TIMESTAMP.info '/usr/*' \
    #     --output-file coverage_$TIMESTAMP.info
    #COVERAGE=$(lcov --summary coverage_$TIMESTAMP.info | \
    #           grep 'lines' | \
    #           awk '{print $2}' | tr -d '%')
    echo "$TIMESTAMP,$COVERAGE" >> "$CSV_FILE"

    sleep 5
done
