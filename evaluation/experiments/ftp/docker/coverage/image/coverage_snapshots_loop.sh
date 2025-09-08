#!/bin/bash

# Start vsftpd in background
#/app/vsftpd /etc/vsftpd/vsftpd.conf &
#VSFTPD_PID=$!

# Loop to capture coverage
BUILD_DIR=/app
while true; do
    TIMESTAMP=$(date +%s)
    #lcov --capture --directory "$BUILD_DIR" --output-file coverage_$TIMESTAMP.info
    #lcov --remove coverage_$TIMESTAMP.info '/usr/*' --output-file coverage_$TIMESTAMP.info
    #COVERAGE=$(lcov --summary coverage_$TIMESTAMP.info | grep 'lines' | awk '{print $2}' | tr -d '%')
    #echo "$TIMESTAMP,$COVERAGE" >> $CSV_FILE
    sleep 5
done

trap "kill $VSFTPD_PID" EXIT