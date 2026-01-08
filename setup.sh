#!/bin/bash

# Hybrid RAG System - Setup Script

echo "================================"
echo "Hybrid RAG System Setup"
echo "================================"
echo ""

# Check Python
if ! command -v python3 &> /dev/null; then
    echo "Error: Python 3 is not installed"
    exit 1
fi

echo "[1/5] Creating virtual environment..."
if [ ! -d "venv" ]; then
    python3 -m venv venv
    echo "Virtual environment created."
else
    echo "Virtual environment already exists."
fi

echo ""
echo "[2/5] Activating virtual environment..."
source venv/bin/activate

echo ""
echo "[3/5] Installing dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

echo ""
echo "[4/5] Setting up environment..."
if [ ! -f ".env" ]; then
    cp .env.example .env
    echo ".env file created. Please edit it with your OpenAI API key."
    echo "Run: nano .env"
else
    echo ".env file already exists."
fi

echo ""
echo "[5/5] Creating data directory..."
if [ ! -d "data/raw" ]; then
    mkdir -p data/raw
    echo "data/raw directory created."
    echo "Please add your DOCX files to data/raw/ directory."
fi

echo ""
echo "================================"
echo "Setup Complete!"
echo "================================"
echo ""
echo "Next steps:"
echo "1. Edit .env file: nano .env"
echo "2. Add DOCX files to data/raw/ directory"
echo "3. Run: ./run_server.sh"
echo ""
