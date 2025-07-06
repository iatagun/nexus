@echo off
echo ===============================================
echo Nexus AI Assistant - Quick Setup (Windows)
echo ===============================================
echo.

echo Checking Python installation...
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Error: Python is not installed or not in PATH
    echo Please install Python 3.8 or higher from https://python.org
    pause
    exit /b 1
)

echo Creating virtual environment...
if exist venv (
    echo Virtual environment already exists
) else (
    python -m venv venv
    if %errorlevel% neq 0 (
        echo Error: Failed to create virtual environment
        pause
        exit /b 1
    )
)

echo Activating virtual environment...
call venv\Scripts\activate.bat

echo Installing dependencies...
pip install --upgrade pip
pip install -e .
if %errorlevel% neq 0 (
    echo Error: Failed to install dependencies
    pause
    exit /b 1
)

echo Setting up environment file...
if not exist .env (
    if exist .env.example (
        copy .env.example .env
    ) else (
        echo # Nexus AI Assistant Configuration > .env
        echo OPENAI_API_KEY=your_openai_api_key_here >> .env
        echo DEBUG_MODE=true >> .env
        echo LOG_LEVEL=info >> .env
    )
)

echo.
echo ===============================================
echo Setup Complete!
echo ===============================================
echo.
echo Next steps:
echo 1. Edit .env file and add your OpenAI API key
echo 2. Run the application:
echo    - Command line: python main.py
echo    - Web interface: streamlit run web_app.py
echo.
echo To activate the environment later:
echo venv\Scripts\activate
echo.
pause
