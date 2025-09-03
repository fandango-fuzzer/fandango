#!/bin/bash

# Path to your Python file
PYTHON_FILE="smtp.py"

# Infinite loop
while true; do
    rm -r ./docker/coverage/coverage
    python3 "$PYTHON_FILE"
    attempt_nr=1
    if [ -e "./coverage_output/attempt_${attempt_nr}_grammar_coverage.csv" ]; then
        while [ -e "./coverage_output/attempt_${attempt_nr}_grammar_coverage.csv" ]; do
            attempt_nr=$((attempt_nr + 1))
        done
        attempt_nr=$((attempt_nr - 1))
    fi

    python3 "convert_series.py" "./docker/coverage/coverage" "./docker/coverage/coverage/series_coverage.csv"
    cp ./docker/coverage/coverage/series_coverage.csv ./coverage_output/attempt_${attempt_nr}_code_coverage.csv
    echo "Script finished. Restarting in 5 seconds..."
    sleep 5
done