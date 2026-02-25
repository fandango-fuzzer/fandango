#!/bin/bash

# Path to your Python file
PYTHON_FILE="dns.py"

# Infinite loop
while true; do
    python3 "$PYTHON_FILE"
    #python3 "multi_run_merger.py" "./coverage_raw" "./coverage/median_grammar_coverage.csv"
    echo "Script finished. Restarting in 5 seconds..."
    sleep 5
done