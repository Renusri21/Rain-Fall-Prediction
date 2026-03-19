@echo off
REM ============================================================================
REM RAINFALL PREDICTION PROJECT - SETUP AND RUN SCRIPT
REM ============================================================================

echo.
echo ============================================================================
echo RAINFALL PREDICTION PROJECT - TensorFlow/Keras Deep Learning
echo ============================================================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python from https://www.python.org/
    pause
    exit /b 1
)

echo [Step 1] Checking Python installation...
python --version
echo.

REM Install required packages
echo [Step 2] Installing required packages from requirements.txt...
echo This may take a few minutes...
echo.
pip install -r requirements.txt
if errorlevel 1 (
    echo ERROR: Failed to install packages
    pause
    exit /b 1
)

echo.
echo [Step 3] Verifying TensorFlow installation...
python -c "import tensorflow; print(f'TensorFlow version: {tensorflow.__version__}')"
if errorlevel 1 (
    echo WARNING: TensorFlow verification failed
    echo Please check your installation
)

echo.
echo ============================================================================
echo RUNNING RAINFALL PREDICTION PROJECT...
echo ============================================================================
echo.

REM Run the main script
python rainfall_prediction.py

if errorlevel 1 (
    echo.
    echo ERROR: Script execution failed
    pause
    exit /b 1
)

echo.
echo ============================================================================
echo PROJECT COMPLETED SUCCESSFULLY!
echo ============================================================================
echo.
echo Output files generated:
echo   - rainfall_model.h5 (trained model)
echo   - scaler.pkl (feature scaler)
echo   - label_encoder.pkl (label encoder)
echo   - rainfall_prediction_analysis.png (visualizations)
echo.
pause
