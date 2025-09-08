#!/bin/bash
# Collect Bind9 coverage every 5 seconds

BUILD_DIR="/home/binduser/bind9"
CSV_FILE="/home/binduser/coverage/coverage.csv"

# Ensure CSV exists
touch "$CSV_FILE"

exec /home/binduser/.local/sbin/named -c /etc/bind/named.conf -f -g -n 1 &
BIND9_PID=$!

trap "kill $BIND9_PID" EXIT

while true; do
    TIMESTAMP=$(date +%s)
    lcov --capture --directory "$BUILD_DIR" --output-file "/home/binduser/coverage/coverage_$TIMESTAMP.info" 2>/dev/null
    COVERAGE=$(lcov --summary "/home/binduser/coverage/coverage_$TIMESTAMP.info" | grep 'lines' | awk '{print $2}' | tr -d '%')
    echo "$TIMESTAMP,$COVERAGE" >> "$CSV_FILE"
    sleep 5
done