#!/bin/bash

# Path to your Python file
PYTHON_FILE="ftp.py"

# Infinite loop
while true; do
    python3 "$PYTHON_FILE"
    echo "Script finished. Restarting in 5 seconds..."
    sleep 5
done