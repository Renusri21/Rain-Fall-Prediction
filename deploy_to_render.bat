@echo off
REM Deploy Flask Rainfall Prediction System to GitHub and Render
REM ============================================================

echo.
echo ╔════════════════════════════════════════════════════════╗
echo ║   🚀 RAINFALL PREDICTION - DEPLOYMENT SCRIPT 🚀        ║
echo ╚════════════════════════════════════════════════════════╝
echo.

REM Check if git is available
where git >nul 2>nul
if %errorlevel% neq 0 (
    echo ❌ Git is not installed or not in PATH
    echo Please install Git from https://git-scm.com/download/win
    pause
    exit /b 1
)

echo [1] Checking git status...
git status >nul 2>nul
if %errorlevel% neq 0 (
    echo ❌ Not a git repository
    echo Please run: git init
    pause
    exit /b 1
)

echo ✓ Git repository found

echo.
echo [2] Adding all files to git...
git add .
if %errorlevel% neq 0 (
    echo ❌ Failed to add files
    pause
    exit /b 1
)
echo ✓ Files added

echo.
echo [3] Committing changes...
git commit -m "Deploy Rainfall Prediction System to Render - %date% %time%"
if %errorlevel% neq 0 (
    echo ℹ️  No changes to commit (already up to date)
) else (
    echo ✓ Changes committed
)

echo.
echo [4] Pushing to GitHub...
git push origin main
if %errorlevel% neq 0 (
    echo ❌ Failed to push to GitHub
    echo Make sure you have:
    echo - Set remote: git remote add origin https://github.com/renusri21/Rain-Fall-Prediction.git
    echo - Created main branch: git branch -M main
    echo - Set credentials: git config --global user.name/email
    pause
    exit /b 1
)
echo ✓ Pushed to GitHub

echo.
echo ╔════════════════════════════════════════════════════════╗
echo ║              ✅ DEPLOYMENT READY                      ║
echo ╚════════════════════════════════════════════════════════╝
echo.
echo Next steps:
echo 1. Go to: https://render.com
echo 2. Sign up (free account)
echo 3. Click "New +" → "Web Service"
echo 4. Connect your GitHub repository
echo 5. Fill in:
echo    - Name: rainfall-prediction
echo    - Build: pip install -r requirements.txt
echo    - Start: python flask_web_app.py
echo 6. Click "Create Web Service"
echo.
echo Your app will be live at:
echo    https://rainfall-prediction.onrender.com
echo.
echo Documentation: RENDER_DEPLOYMENT_GUIDE.md
echo.
pause
