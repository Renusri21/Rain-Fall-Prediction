# Flask Web Application - Complete Deployment Guide

## 📋 Table of Contents
1. [Quick Start](#quick-start)
2. [System Requirements](#system-requirements)
3. [Installation Steps](#installation-steps)
4. [Running the Application](#running-the-application)
5. [Testing the Application](#testing-the-application)
6. [API Documentation](#api-documentation)
7. [Troubleshooting](#troubleshooting)
8. [Production Deployment](#production-deployment)

---

## 🚀 Quick Start

### Windows Users
1. Open Command Prompt (cmd.exe)
2. Navigate to project directory
3. Run: `run_flask_app.bat`

### Linux/macOS Users
```bash
python flask_web_app.py
```

Then open your browser to: **http://localhost:5000/**

---

## 💻 System Requirements

### Minimum Requirements
- **OS:** Windows 10+, macOS 10.14+, or Ubuntu 18.04+
- **Python:** 3.7 or higher
- **RAM:** 512 MB
- **Disk Space:** 200 MB (with dependencies)

### Recommended
- **Python:** 3.9 or 3.10
- **RAM:** 2 GB
- **Disk Space:** 500 MB

### Browser Support
- Chrome/Chromium (recommended)
- Firefox
- Safari
- Edge
- Any modern browser with JavaScript support

---

## 📥 Installation Steps

### Step 1: Verify Python Installation

```bash
python --version
```

Should output: `Python 3.x.x` (where x ≥ 7)

If Python is not found:
- Download from: https://www.python.org/
- Install with "Add Python to PATH" checked
- Restart your terminal

### Step 2: Install Required Packages

Option A - Using requirements.txt:
```bash
pip install -r requirements.txt
```

Option B - Manual installation:
```bash
pip install flask numpy pandas scikit-learn
```

### Step 3: Verify Installation

Run the setup verification script:
```bash
python verify_flask_setup.py
```

Expected output:
```
✓ PASS: Python 3.9 is supported
✓ PASS: Flask is installed
✓ PASS: Model loaded successfully
...
✓✓✓ ALL CHECKS PASSED ✓✓✓
```

### Step 4: Verify Model Files

Ensure these files exist in the project directory:
- ✓ `rainfall_model.pkl`
- ✓ `scaler.pkl`
- ✓ `label_encoder.pkl`
- ✓ `templates/index.html`

If missing, regenerate them:
```bash
python rainfall_prediction_sklearn.py
```

---

## 🎯 Running the Application

### Method 1: Windows Batch Script (Easiest)
```batch
run_flask_app.bat
```

### Method 2: Command Line
```bash
python flask_web_app.py
```

### Method 3: Python IDE
Open `flask_web_app.py` in your IDE and click "Run"

### Method 4: Import as Module
```python
from flask_web_app import app

if __name__ == '__main__':
    app.run(debug=True)
```

### Expected Output
```
======================================================================
                  🌧️  RAINFALL PREDICTION SYSTEM  🌧️
======================================================================

LOADING MACHINE LEARNING MODEL AND UTILITIES
======================================================================

[1] Loading trained model...
✓ Model loaded successfully
  Model type: MLPClassifier

[2] Loading feature scaler...
✓ Scaler loaded successfully

[3] Loading label encoder...
✓ Label encoder loaded successfully
  Classes: ['No', 'Yes']

======================================================================
✓ ALL MODELS LOADED SUCCESSFULLY
======================================================================

🚀 STARTING FLASK APPLICATION...

======================================================================
📍 Web Interface: http://localhost:5000/
📍 API Endpoint:  http://localhost:5000/predict
📍 Health Check:  http://localhost:5000/api/health
📍 Model Info:    http://localhost:5000/api/model-info
======================================================================

✓ Application is running!
✓ Press CTRL+C to stop the server
```

---

## ✅ Testing the Application

### Option 1: Automated Testing
```bash
python test_flask_api.py
```

This runs 5 prediction tests + 4 validation tests.

### Option 2: Web Interface Testing

1. Open browser to `http://localhost:5000/`
2. Enter test values:
   ```
   Temperature: 28
   Humidity: 75
   Air Pressure: 1000
   Wind Speed: 12
   ```
3. Click "Predict Rainfall"
4. Should see: "☔ Rainfall Expected" with confidence percentage

### Option 3: API Testing with cURL

```bash
curl -X POST http://localhost:5000/predict \
  -H "Content-Type: application/json" \
  -d '{
    "temperature": 25,
    "humidity": 65,
    "pressure": 1015,
    "wind_speed": 8
  }'
```

Expected response:
```json
{
  "success": true,
  "prediction": "No",
  "confidence": 72.5,
  "probabilities": {
    "no_rain": 72.5,
    "rain": 27.5
  },
  "input": {
    "temperature": 25,
    "humidity": 65,
    "pressure": 1015,
    "wind_speed": 8
  },
  "timestamp": "2026-03-19T12:34:56.789123"
}
```

### Option 4: API Testing with Python
```python
import requests

url = "http://localhost:5000/predict"
data = {
    "temperature": 25,
    "humidity": 65,
    "pressure": 1015,
    "wind_speed": 8
}

response = requests.post(url, json=data)
print(response.json())
```

### Test Cases

| Case | Temperature | Humidity | Pressure | Wind | Expected |
|------|-------------|----------|----------|------|----------|
| Rainy | 28°C | 75% | 1000 hPa | 12 | Rain |
| Sunny | 30°C | 40% | 1020 hPa | 5 | No Rain |
| Cold | 5°C | 30% | 1025 hPa | 3 | No Rain |

---

## 📡 API Documentation

### Base URL
```
http://localhost:5000
```

### Endpoints

#### 1. GET / (Home Page)
- **Description:** Serve the web interface
- **Method:** GET
- **Request:** None
- **Response:** HTML page

#### 2. POST /predict (Make Prediction)
- **Description:** Make a rainfall prediction
- **Method:** POST
- **Content-Type:** application/json

**Request Body:**
```json
{
  "temperature": float,      // -50 to 60 (°C)
  "humidity": float,         // 0 to 100 (%)
  "pressure": float,         // 800 to 1100 (hPa)
  "wind_speed": float        // 0 to 100 (km/h)
}
```

**Success Response (200):**
```json
{
  "success": true,
  "prediction": "Yes" | "No",
  "confidence": number,      // 0-100%
  "probabilities": {
    "no_rain": number,
    "rain": number
  },
  "input": { /* echo of input */ },
  "timestamp": "ISO timestamp",
  "model_info": {
    "name": "MLPClassifier (Scikit-learn)",
    "accuracy": "70%",
    "features": ["Temperature", "Humidity", "Air Pressure", "Wind Speed"]
  }
}
```

**Error Response (400/500):**
```json
{
  "success": false,
  "error": "Error description"
}
```

#### 3. GET /api/health (Health Check)
- **Description:** Check if application is running
- **Method:** GET
- **Response:**
```json
{
  "status": "healthy" | "unhealthy",
  "model_loaded": true | false,
  "timestamp": "ISO timestamp"
}
```

#### 4. GET /api/model-info (Model Information)
- **Description:** Get model details and performance metrics
- **Method:** GET
- **Response:**
```json
{
  "model_loaded": true,
  "model_type": "MLPClassifier",
  "model_name": "Rainfall Prediction Neural Network",
  "framework": "scikit-learn",
  "test_accuracy": "70%",
  "training_accuracy": "77.5%",
  "convergence": "27 epochs",
  "training_time": "0.03 seconds",
  "features": ["Temperature (°C)", "Humidity (%)", "Air Pressure (hPa)", "Wind Speed (km/h)"],
  "output_classes": ["No", "Yes"],
  "version": "1.0",
  "created": "March 18, 2026"
}
```

---

## 🛠️ Troubleshooting

### Issue: "ModuleNotFoundError: No module named 'flask'"

**Solution:**
```bash
pip install flask
```

Or use requirements.txt:
```bash
pip install -r requirements.txt
```

### Issue: "Model not loaded" Error

**Cause:** Model files (.pkl) not found

**Solution:**
```bash
# Regenerate model files
python rainfall_prediction_sklearn.py
```

Ensure these files are in project root:
- `rainfall_model.pkl`
- `scaler.pkl`
- `label_encoder.pkl`

### Issue: "Port 5000 already in use"

**Solution 1:** Stop other processes using port 5000
```bash
# Windows - Find process on port 5000
netstat -ano | findstr :5000

# Kill process (replace PID with actual process ID)
taskkill /PID <PID> /F
```

**Solution 2:** Use different port

Edit `flask_web_app.py`:
```python
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)  # Change to 5001
```

Then access: `http://localhost:5001/`

### Issue: "templates/index.html not found"

**Solution:**
```bash
# Verify directory structure
dir /s templates
# Should show: templates\index.html

# If missing, re-download or recreate the file
```

### Issue: Browser shows "Cannot GET /"

**Cause:** Flask app not running or wrong URL

**Solution:**
1. Verify Flask is running (check console for "Running on...")
2. Open exact URL: `http://localhost:5000/`
3. Not `http://0.0.0.0:5000/` (use localhost instead)

### Issue: Prediction returns very low accuracy

**Cause:** Model may not have trained properly

**Solution:**
```bash
# Retrain the model
python rainfall_prediction_sklearn.py

# Verify training output shows ~70% test accuracy
```

---

## 🌐 Production Deployment

### Option 1: Using Gunicorn (Linux/macOS)

Install:
```bash
pip install gunicorn
```

Run:
```bash
gunicorn -w 4 -b 0.0.0.0:5000 flask_web_app:app
```

Parameters:
- `-w 4` - Number of worker processes
- `-b 0.0.0.0:5000` - Bind to all interfaces on port 5000

### Option 2: Using Waitress (Windows)

Install:
```bash
pip install waitress
```

Create `run_production.py`:
```python
from waitress import serve
from flask_web_app import app

if __name__ == '__main__':
    serve(app, host='0.0.0.0', port=5000)
```

Run:
```bash
python run_production.py
```

### Option 3: Docker Deployment

Create `Dockerfile`:
```dockerfile
FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

CMD ["python", "flask_web_app.py"]

EXPOSE 5000
```

Build and run:
```bash
docker build -t rainfall-app .
docker run -p 5000:5000 rainfall-app
```

### Option 4: Cloud Deployment (Heroku)

1. Install Heroku CLI
2. Create `Procfile`:
   ```
   web: gunicorn flask_web_app:app
   ```
3. Deploy:
   ```bash
   heroku login
   heroku create your-app-name
   git push heroku main
   ```

### Deployment Checklist

- [ ] Python 3.7+ installed
- [ ] All dependencies installed (`pip install -r requirements.txt`)
- [ ] Model files present (rainfall_model.pkl, scaler.pkl, label_encoder.pkl)
- [ ] templates/index.html exists
- [ ] flask_web_app.py is configured correctly
- [ ] Port 5000 is accessible/open
- [ ] Firewall allows inbound connections (if needed)
- [ ] Environment is production-ready (debug=False)

### Security Considerations

1. **Set debug=False in production:**
   ```python
   app.run(debug=False)
   ```

2. **Use HTTPS:**
   ```python
   from flask_talisman import Talisman
   Talisman(app)
   ```

3. **Add rate limiting:**
   ```bash
   pip install flask-limiter
   ```

4. **Validate all inputs:** Already implemented in flask_web_app.py

---

## 📞 Support & Additional Resources

- Flask Documentation: https://flask.palletsprojects.com/
- Scikit-learn: https://scikit-learn.org/
- Model Training: See `rainfall_prediction_sklearn.py`
- API Examples: See `deploy_model.py`

---

## 🎓 Project Information

- **Project:** Rainfall Prediction System
- **Framework:** Flask 2.0+
- **ML Model:** scikit-learn MLPClassifier
- **Features:** 4 weather parameters
- **Output:** Binary classification (Rain/No Rain)
- **Accuracy:** 70% (test), 77.5% (training)
- **Version:** 1.0
- **Last Updated:** March 19, 2026

---

**Created by:** AI Assistant  
**License:** MIT
