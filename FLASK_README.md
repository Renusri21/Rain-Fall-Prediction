# 🌧️ Rainfall Prediction System - Flask Web Application

## Overview

This is a complete Flask web application for rainfall prediction using a trained machine learning model (Neural Network - MLPClassifier).

**Features:**
- ✅ Pre-trained ML model loaded from pickle files
- ✅ Beautiful, responsive web interface
- ✅ Real-time form validation
- ✅ REST API endpoints for predictions
- ✅ Error handling and user feedback
- ✅ Mobile-friendly design

---

## Project Structure

```
RainfallPredictionProject/
├── flask_web_app.py              # Main Flask application
├── flask_api.py                  # Alternative Flask API
├── rainfall_model.pkl            # Trained model (serialized)
├── scaler.pkl                    # Feature scaler
├── label_encoder.pkl             # Label encoder
├── rainfall_data.csv             # Sample weather data
├── templates/
│   └── index.html                # Web interface
├── requirements.txt              # Python dependencies
└── README.md                      # Project documentation
```

---

## Prerequisites

### 1. Python Installation
- Python 3.7 or higher
- Ensure Python is added to your system PATH

### 2. Required Dependencies

Install the required packages:

```bash
pip install flask numpy pandas scikit-learn
```

Or use requirements.txt:

```bash
pip install -r requirements.txt
```

### 3. Model Files

The application requires three model files in the project root directory:
- `rainfall_model.pkl` - Trained neural network model
- `scaler.pkl` - Feature normalization scaler  
- `label_encoder.pkl` - Target variable encoder

These files should already be present if you've run `rainfall_prediction_sklearn.py`.

---

## Running the Flask Application

### Method 1: Using Flask Command Line

```bash
# Navigate to project directory
cd C:\RainfallPredictionProject

# Run the Flask app
python flask_web_app.py
```

### Method 2: Using Python Directly

```bash
python flask_web_app.py
```

### Expected Output

```
════════════════════════════════════════════════════════════════════════════════
                    🌧️  RAINFALL PREDICTION SYSTEM  🌧️
====════════════════════════════════════════════════════════════════════════════

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

## Accessing the Application

### Web Interface
- **URL:** http://localhost:5000/
- **Description:** Beautiful web form for rainfall prediction
- **Features:**
  - Input fields: Temperature, Humidity, Air Pressure, Wind Speed
  - Real-time validation with error messages
  - Animated result display
  - Shows confidence percentage

### API Endpoints

#### 1. Make a Prediction
- **Endpoint:** `POST /predict`
- **URL:** http://localhost:5000/predict
- **Content-Type:** `application/json`

**Request Example:**
```json
{
  "temperature": 28,
  "humidity": 70,
  "pressure": 1012,
  "wind_speed": 9
}
```

**Response Example (Rain Prediction):**
```json
{
  "success": true,
  "prediction": "Yes",
  "confidence": 85.3,
  "probabilities": {
    "no_rain": 14.7,
    "rain": 85.3
  },
  "input": {
    "temperature": 28,
    "humidity": 70,
    "pressure": 1012,
    "wind_speed": 9
  },
  "timestamp": "2026-03-19T12:34:56.789123",
  "model_info": {
    "name": "MLPClassifier (Scikit-learn)",
    "accuracy": "70%",
    "features": ["Temperature", "Humidity", "Air Pressure", "Wind Speed"]
  }
}
```

#### 2. Get Model Information
- **Endpoint:** `GET /api/model-info`
- **URL:** http://localhost:5000/api/model-info
- **Response:** JSON with model details, architecture, and performance metrics

#### 3. Health Check
- **Endpoint:** `GET /api/health`
- **URL:** http://localhost:5000/api/health
- **Response:** Health status and timestamp

---

## Testing the Application

### Test Case 1: Rainy Conditions
Weather: Warm, Humid, Lower Pressure
```
Temperature: 28°C
Humidity: 75%
Pressure: 1000 hPa
Wind Speed: 12 km/h
Expected: ☔ Rainfall Expected
```

### Test Case 2: Dry Conditions
Weather: Warm, Dry, High Pressure
```
Temperature: 30°C
Humidity: 40%
Pressure: 1020 hPa
Wind Speed: 5 km/h
Expected: ☀️ No Rainfall
```

### Test Case 3: Cold Conditions
Weather: Cold, Dry, High Pressure
```
Temperature: 5°C
Humidity: 30%
Pressure: 1025 hPa
Wind Speed: 3 km/h
Expected: ☀️ No Rainfall
```

---

## Input Validation

The application validates all input fields with the following constraints:

| Field | Min | Max | Unit |
|-------|-----|-----|------|
| Temperature | -50 | 60 | °C |
| Humidity | 0 | 100 | % |
| Air Pressure | 800 | 1100 | hPa |
| Wind Speed | 0 | 100 | km/h |

---

## Error Handling

The application handles various error scenarios:

1. **Missing Model Files**
   - Error message indicates which files are missing
   - Instructions provided to regenerate models

2. **Invalid Input Values**
   - Out-of-range values are rejected
   - Specific error message for each field

3. **Server Errors**
   - JSON error response with description
   - HTTP status codes for client differentiation

4. **Network Issues**
   - Frontend displays error message
   - User can retry the prediction

---

## Troubleshooting

### Issue: "Model not loaded" Error

**Cause:** Model files not found in project directory

**Solution:**
```bash
# Regenerate model files
python rainfall_prediction_sklearn.py
```

### Issue: "Port 5000 already in use"

**Cause:** Another application is using port 5000

**Solution:** Edit `flask_web_app.py` and change port:
```python
app.run(host='0.0.0.0', port=5001)  # Change 5000 to 5001
```

### Issue: "Flask not found" Error

**Cause:** Flask is not installed

**Solution:**
```bash
pip install flask
```

### Issue: CORS Errors

**Cause:** Frontend and backend on different origins

**Solution:** Install Flask-CORS:
```bash
pip install flask-cors
```

Then add to `flask_web_app.py`:
```python
from flask_cors import CORS
CORS(app)
```

---

## Performance Characteristics

- **Model Type:** MLPClassifier (Neural Network)
- **Training Accuracy:** 77.5%
- **Test Accuracy:** 70%
- **Prediction Time:** ~50ms per request
- **Model Size:** ~3 KB (pkl serialized)
- **Features:** 4 weather parameters
- **Output:** Binary classification (Rain/No Rain)

---

## Advanced Configuration

### Running on Different Host/Port

Edit `flask_web_app.py`:
```python
if __name__ == '__main__':
    app.run(
        host='192.168.1.100',  # Your IP address
        port=8000,              # Custom port
        debug=False             # Production mode
    )
```

### Running in Debug Mode

For development with auto-reload:
```python
app.run(debug=True)
```

### Running in Production

For production deployment, use a production server like Gunicorn:
```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 flask_web_app:app
```

---

## API Usage Examples

### Using Python Requests Library

```python
import requests
import json

url = "http://localhost:5000/predict"
data = {
    "temperature": 25,
    "humidity": 65,
    "pressure": 1015,
    "wind_speed": 8
}

response = requests.post(url, json=data)
print(json.dumps(response.json(), indent=2))
```

### Using cURL

```bash
curl -X POST http://localhost:5000/predict \
  -H "Content-Type: application/json" \
  -d '{"temperature": 25, "humidity": 65, "pressure": 1015, "wind_speed": 8}'
```

### Using Fetch (JavaScript)

```javascript
fetch('http://localhost:5000/predict', {
  method: 'POST',
  headers: {'Content-Type': 'application/json'},
  body: JSON.stringify({
    temperature: 25,
    humidity: 65,
    pressure: 1015,
    wind_speed: 8
  })
})
.then(response => response.json())
.then(data => console.log(data))
```

---

## Files Overview

### flask_web_app.py
Complete Flask web application with:
- Model loading with error handling
- Home route (`GET /`)
- Prediction endpoint (`POST /predict`)
- Health check endpoint (`GET /api/health`)
- Model info endpoint (`GET /api/model-info`)
- Comprehensive input validation
- JSON response formatting

### index.html
Professional web interface featuring:
- Responsive design
- Real-time input validation
- Animated UI elements
- Error message display
- Loading spinner
- Result display with prediction
- Mobile-friendly layout
- CSS gradient background
- Form clear button

### Model Files
- `rainfall_model.pkl` - Trained neural network
- `scaler.pkl` - Feature normalization (StandardScaler)
- `label_encoder.pkl` - Target encoding (Yes/No → 1/0)

---

## System Requirements

- **OS:** Windows, macOS, or Linux
- **Python:** 3.7+
- **RAM:** Minimum 512MB (1GB recommended)
- **Disk:** ~100MB for dependencies
- **Browser:** Modern browser (Chrome, Firefox, Safari, Edge)

---

## Support & Documentation

For more information:
- See `README.md` for project overview
- See `rainfall_prediction_sklearn.py` for model training details
- See `deploy_model.py` for batch prediction examples
- Check Flask documentation: https://flask.palletsprojects.com/

---

## Author
AI Assistant

## Version
1.0

## Last Updated
March 19, 2026
