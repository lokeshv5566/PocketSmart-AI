@echo off
cd /d "%~dp0"
echo Creating Python virtual environment...
py -3.11 -m venv .venv
if errorlevel 1 (
  echo Failed to create the virtual environment.
  echo Make sure Python 3.11 is installed and available as ^"py -3.11^".
  pause
  exit /b 1
)
call ".venv\Scripts\activate.bat"
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
if not exist ".env" copy ".env.example" ".env" >nul
echo.
echo Setup complete.
echo Edit .env and paste your Gemini API key, then run run.bat
pause
