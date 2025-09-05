#!/bin/bash

# Path to your Python file
PYTHON_FILE="smtp.py"

# Infinite loop
while true; do
    mkdir -p ./coverage_raw
    mkdir -p ./coverage
    python3 "$PYTHON_FILE"
    attempt_nr=1
    if [ -e "./coverage_raw/attempt_${attempt_nr}_grammar_coverage.csv" ]; then
        while [ -e "./coverage_raw/attempt_${attempt_nr}_grammar_coverage.csv" ]; do
            attempt_nr=$((attempt_nr + 1))
        done
        attempt_nr=$((attempt_nr - 1))
    fi

    python3 "multi_run_merger.py" "./coverage_raw" "./coverage/median_grammar_coverage.csv"
    echo "Script finished. Restarting in 5 seconds..."
    sleep 5
done