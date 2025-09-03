#!/bin/bash

mkdir -p coverage_snapshots/gcda
CSV_FILE=coverage_snapshots/summary.csv

if [ ! -f "$CSV_FILE" ]; then
    echo "timestamp,coverage" > "$CSV_FILE"
fi

# Export LLVM coverage environment variables for forked processes
export LLVM_PROFILE_FILE="/app/coverage_snapshots/gcda/coverage-%p.profraw"

# Start vsftpd in foreground
/app/vsftpd /etc/vsftpd/vsftpd.conf &
VSFTPD_PID=$!
trap "kill $VSFTPD_PID" EXIT

# Loop to generate coverage report periodically
while true; do
    sleep 5
    TIMESTAMP=$(date +%s)

    if compgen -G "/app/coverage_snapshots/gcda/*.profraw" > /dev/null; then
        llvm-profdata merge -sparse /app/coverage_snapshots/gcda/*.profraw -o /app/coverage_snapshots/coverage.profdata
        llvm-cov report /app/vsftpd -instr-profile=/app/coverage_snapshots/coverage.profdata | tee /app/coverage_snapshots/coverage_$TIMESTAMP.txt
        COVERAGE=$(llvm-cov report /app/vsftpd -instr-profile=/app/coverage_snapshots/coverage.profdata | grep -E 'lines:' | awk '{print $2}' | tr -d '%')
        echo "$TIMESTAMP,$COVERAGE" >> $CSV_FILE
    fi
done