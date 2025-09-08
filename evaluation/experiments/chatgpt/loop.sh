#!/bin/bash

# Path to your Python file
PYTHON_FILE="gpt_novel.py"

# Infinite loop
while true; do
    mkdir -p ./coverage_raw
    python3 "$PYTHON_FILE"
    echo "Script finished. Restarting in 5 seconds..."
    sleep 5
done