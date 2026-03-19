@echo off
REM ============================================================================
REM Rainfall Prediction System - Flask Web Application Launcher
REM ============================================================================
REM This batch script starts the Flask web application on Windows
REM

echo.
echo ============================================================================
echo              RAINFALL PREDICTION SYSTEM - FLASK WEB APP
echo ============================================================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo.
    echo Please install Python 3.7 or higher from https://www.python.org/
    echo Make sure to check "Add Python to PATH" during installation
    echo.
    pause
    exit /b 1
)

echo Checking Python version...
python --version
echo.

REM Check if Flask is installed
python -c "import flask" >nul 2>&1
if errorlevel 1 (
    echo Flask is not installed. Installing now...
    pip install flask
    if errorlevel 1 (
        echo ERROR: Failed to install Flask
        pause
        exit /b 1
    )
)

echo.
echo Checking for required model files...
if not exist "rainfall_model.pkl" (
    echo ERROR: rainfall_model.pkl not found!
    echo.
    echo Please ensure the model has been trained by running:
    echo   python rainfall_prediction_sklearn.py
    echo.
    pause
    exit /b 1
)

if not exist "scaler.pkl" (
    echo ERROR: scaler.pkl not found!
    pause
    exit /b 1
)

if not exist "label_encoder.pkl" (
    echo ERROR: label_encoder.pkl not found!
    pause
    exit /b 1
)

if not exist "templates\index.html" (
    echo ERROR: templates\index.html not found!
    pause
    exit /b 1
)

echo ✓ All required files found!
echo.

echo ============================================================================
echo Starting Flask application...
echo ============================================================================
echo.
echo The application will be available at:
echo   http://localhost:5000/
echo.
echo API Endpoints:
echo   - POST http://localhost:5000/predict
echo   - GET  http://localhost:5000/api/health
echo   - GET  http://localhost:5000/api/model-info
echo.
echo Press CTRL+C to stop the server
echo.
echo ============================================================================
echo.

python flask_web_app.py

pause
