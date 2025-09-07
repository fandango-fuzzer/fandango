#!/bin/bash
BUILD_DIR=/home/binduser/bind9
CSV_FILE=/home/binduser/coverage.csv

while true; do
    TIMESTAMP=$(date +%s)
    lcov --capture --directory "$BUILD_DIR" --output-file coverage_$TIMESTAMP.info
    COVERAGE=$(lcov --summary coverage_$TIMESTAMP.info | grep 'lines' | awk '{print $2}' | tr -d '%')
    echo "$TIMESTAMP,$COVERAGE" >> $CSV_FILE
    sleep 10
done