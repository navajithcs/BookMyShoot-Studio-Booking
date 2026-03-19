@echo off
REM BookMyShoot - Startup Script for Windows

echo.
echo ============================================================
echo  BookMyShoot - Full Stack Application
echo ============================================================
echo.

set PROJECT_ROOT=%~dp0
set VENV_PYTHON=%PROJECT_ROOT%.venv\Scripts\python.exe

if not exist "%VENV_PYTHON%" (
    echo ERROR: Virtual environment not found!
    echo Please run configure_python_environment first.
    pause
    exit /b 1
)

echo Starting services...
echo.

REM Kill any existing Flask processes on port 5000
echo Checking for existing servers on port 5000...
for /f "tokens=5" %%p in ('netstat -ano ^| findstr ":5000" ^| findstr "LISTENING"') do (
    echo Stopping old process PID=%%p...
    taskkill /PID %%p /F >nul 2>&1
)
timeout /t 2 /nobreak >nul

REM Start Backend
echo Starting Backend (Flask) on http://localhost:5000...
start "BookMyShoot Backend" "%VENV_PYTHON%" "%PROJECT_ROOT%backend\app.py" --no-reload

REM Wait a moment for backend to start
timeout /t 2 /nobreak

REM Start Frontend
echo Starting Frontend (HTTP Server) on http://localhost:5173...
start "BookMyShoot Frontend" "%VENV_PYTHON%" "%PROJECT_ROOT%serve_frontend.py"

echo.
echo ============================================================
echo  All servers started!
echo ============================================================
echo.
echo Access the application:
echo   Frontend: http://localhost:5173
echo   Backend:  http://localhost:5000
echo.
echo Close the command windows to stop the servers.
echo.
pause
