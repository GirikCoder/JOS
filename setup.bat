@echo off
echo ===================================================
echo Setting up Jarvis Operating System Environment
echo ===================================================

echo.
echo [1/4] Checking for virtual environment...
if not exist venv (
    echo Creating a new virtual environment...
    python -m venv venv
) else (
    echo Virtual environment already exists. Skipping creation.
)

echo.
echo [2/4] Activating virtual environment...
call venv\Scripts\activate.bat

echo.
echo [3/4] Installing or updating required modules...
python -m pip install --upgrade pip
pip install -r requirements.txt

echo.
echo [4/4] Ensuring spaCy English NLP model is installed...
python -m spacy download en_core_web_md

echo.
echo ===================================================
echo Setup Complete! 
echo To start working, run: venv\Scripts\activate
echo ===================================================
pause