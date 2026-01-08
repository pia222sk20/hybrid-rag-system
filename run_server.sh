#!/bin/bash

# Run Hybrid RAG System API Server

echo "================================"
echo "Starting Hybrid RAG System"
echo "================================"
echo ""

# Activate virtual environment
source venv/bin/activate

echo "Server starting on http://localhost:8000"
echo "API Documentation: http://localhost:8000/docs"
echo ""
echo "Press Ctrl+C to stop the server"
echo ""

# Start server with auto-reload
uvicorn api.main:app --reload --host 0.0.0.0 --port 8000
