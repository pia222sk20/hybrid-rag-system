@echo off
REM Hybrid RAG System - Setup and Run Script

echo ================================
echo Hybrid RAG System Setup
echo ================================
echo.

REM Check Python
python --version >nul 2>&1
if errorlevel 1 (
    echo Error: Python is not installed or not in PATH
    pause
    exit /b 1
)

echo [1/5] Creating virtual environment...
if not exist venv (
    python -m venv venv
    echo Virtual environment created.
) else (
    echo Virtual environment already exists.
)

echo.
echo [2/5] Activating virtual environment...
call venv\Scripts\activate.bat

echo.
echo [3/5] Installing dependencies...
pip install --upgrade pip
pip install -r requirements.txt

echo.
echo [4/5] Setting up environment...
if not exist .env (
    copy .env.example .env
    echo .env file created. Please edit it with your OpenAI API key.
    echo Opening .env file...
    notepad .env
) else (
    echo .env file already exists.
)

echo.
echo [5/5] Creating data directory...
if not exist data\raw (
    mkdir data\raw
    echo data\raw directory created.
    echo Please add your DOCX files to data\raw\ directory.
)

echo.
echo ================================
echo Setup Complete!
echo ================================
echo.
echo Next steps:
echo 1. Make sure your OpenAI API key is in .env file
echo 2. Add DOCX files to data\raw\ directory
echo 3. Run: run_server.bat
echo.
pause
