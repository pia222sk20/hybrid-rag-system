@echo off
REM Hybrid RAG System - Conda Setup Script for Windows

echo ================================
echo Hybrid RAG System - Conda Setup
echo ================================
echo.

REM Check Conda installation
conda --version >nul 2>&1
if errorlevel 1 (
    echo Error: Conda is not installed or not in PATH
    echo Please install Anaconda or Miniconda first:
    echo https://www.anaconda.com/download
    echo https://docs.conda.io/en/latest/miniconda.html
    pause
    exit /b 1
)

echo [1/6] Conda version:
conda --version
echo.

echo [2/6] Creating conda environment 'hybrid-rag' with Python 3.10...
conda create -n hybrid-rag python=3.10 pip -y

if errorlevel 1 (
    echo Error: Failed to create conda environment
    pause
    exit /b 1
)

echo.
echo [3/6] Activating conda environment...
call conda activate hybrid-rag

if errorlevel 1 (
    echo Error: Failed to activate conda environment
    echo Try running: conda init
    pause
    exit /b 1
)

echo.
echo [4/6] Upgrading pip...
python -m pip install --upgrade pip

echo.
echo [5/6] Installing project dependencies...
pip install -r requirements.txt

if errorlevel 1 (
    echo Error: Failed to install dependencies
    pause
    exit /b 1
)

echo.
echo [6/6] Setting up environment file...
if not exist .env (
    copy .env.example .env
    echo .env file created. Opening for editing...
    timeout /t 2 >nul
    notepad .env
) else (
    echo .env file already exists.
)

echo.
echo Creating data directory...
if not exist data\raw (
    mkdir data\raw
    echo data\raw directory created.
)

echo.
echo ================================
echo Setup Complete! 🎉
echo ================================
echo.
echo Conda environment 'hybrid-rag' is ready!
echo.
echo Next steps:
echo 1. Make sure your OpenAI API key is in .env file
echo 2. Add DOCX files to data\raw\ directory
echo 3. Activate environment: conda activate hybrid-rag
echo 4. Run server: uvicorn api.main:app --reload
echo.
echo Or simply run: run_server_conda.bat
echo.
pause
