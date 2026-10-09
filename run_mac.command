#!/bin/bash
cd "$(dirname "$0")"

echo "=========================================="
echo " Starting PinNote on macOS..."
echo "=========================================="

# Check if python3 is installed
if ! command -v python3 &> /dev/null; then
    echo "Python 3 is required. Please install Python from https://python.org or run 'xcode-select --install'"
    read -p "Press Enter to exit..."
    exit 1
fi

# Set up virtual environment if not present
if [ ! -d "venv" ]; then
    echo "Setting up Python environment (first run only)..."
    python3 -m venv venv
    ./venv/bin/pip install --upgrade pip
    ./venv/bin/pip install -r requirements.txt
fi

# Run PinNote
./venv/bin/python pin_note.py
