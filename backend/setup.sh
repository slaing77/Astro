#!/bin/bash

# Create venv if it doesn't exist
if [ ! -d "venv" ]; then
  echo "🔹 Creating virtual environment..."
  python -m venv venv
fi

# Activate venv
source venv/bin/activate

# Install requirements
echo "🔹 Installing dependencies..."
pip install -r requirements.txt

echo "✅ Virtual environment is ready!"
