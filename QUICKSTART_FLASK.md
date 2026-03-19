# 🚀 RAINFALL PREDICTION SYSTEM - FLASK WEB APP
## QUICK START GUIDE

---

## ⚡ 30-Second Start (Windows)

```batch
# 1. Open Command Prompt
# 2. Navigate to project
cd C:\RainfallPredictionProject

# 3. Run the app
run_flask_app.bat

# 4. Open browser
http://localhost:5000/
```

---

## ⚡ 30-Second Start (Mac/Linux)

```bash
# 1. Open Terminal
# 2. Navigate to project
cd path/to/RainfallPredictionProject

# 3. Install Flask if needed
pip install flask

# 4. Run the app
python flask_web_app.py

# 5. Open browser
http://localhost:5000/
```

---

## 📋 What You Get

✅ **Web Interface** - Beautiful prediction form  
✅ **REST API** - JSON endpoints for predictions  
✅ **ML Model** - Trained neural network (70% accuracy)  
✅ **Validation** - Real-time input checking  
✅ **Error Handling** - Comprehensive error messages  
✅ **Mobile Ready** - Responsive design  

---

## 🔧 Requirements

- **Python 3.7+**
- **Flask** (will install automatically)
- **NumPy, Pandas, Scikit-learn** (will install automatically)

---

## 📡 What's Running

| Component | URL | Purpose |
|-----------|-----|---------|
| Web Interface | http://localhost:5000/ | Beautiful UI for predictions |
| API Endpoint | http://localhost:5000/predict | Make predictions via JSON |
| Health Check | http://localhost:5000/api/health | Check if app is running |
| Model Info | http://localhost:5000/api/model-info | Get model details |

---

## 🎯 Make Your First Prediction

### Using Web Browser
1. Go to http://localhost:5000/
2. Enter values:
   - **Temperature:** 28°C
   - **Humidity:** 75%
   - **Pressure:** 1000 hPa
   - **Wind Speed:** 12 km/h
3. Click **"Predict Rainfall"**
4. See result: "☔ Rainfall Expected (85%)"

### Using API (cURL)
```bash
curl -X POST http://localhost:5000/predict \
  -H "Content-Type: application/json" \
  -d '{"temperature": 28, "humidity": 75, "pressure": 1000, "wind_speed": 12}'
```

### Using Python
```python
import requests

response = requests.post('http://localhost:5000/predict', json={
    'temperature': 28,
    'humidity': 75,
    'pressure': 1000,
    'wind_speed': 12
})
print(response.json())
```

---

## 📂 Project Files

```
RainfallPredictionProject/
├── flask_web_app.py           ← Main Flask app (START THIS)
├── templates/index.html       ← Web interface
├── rainfall_model.pkl         ← Trained model
├── scaler.pkl                 ← Feature scaler
├── label_encoder.pkl          ← Label encoder
├── run_flask_app.bat          ← Windows launcher
├── verify_flask_setup.py      ← Verify installation
├── test_flask_api.py          ← Run tests
└── FLASK_README.md            ← Full documentation
```

---

## ✅ Troubleshooting

### Problem: "Flask not found"
```bash
pip install flask
```

### Problem: "Port 5000 in use"
```bash
# Windows - find & kill process
netstat -ano | findstr :5000
taskkill /PID <PID> /F

# Or edit flask_web_app.py, change port=5001
```

### Problem: "Model not found"
```bash
python rainfall_prediction_sklearn.py
```

### Problem: Cannot open http://localhost:5000
- Make sure Flask is running (check console)
- Try `http://127.0.0.1:5000/` instead
- Browser might have cached old result

---

## 📝 Test Script

Verify everything works:
```bash
python verify_flask_setup.py
```

Run automated tests:
```bash
python test_flask_api.py
```

---

## 🎓 How It Works

1. **You enter weather data** in the web form
2. **Frontend validates inputs** using JavaScript
3. **Data sent to Flask** via JSON POST request
4. **Flask preprocesses** the data (normalization)
5. **Model makes prediction** using neural network
6. **Result displayed** with confidence percentage

---

## 📊 Model Details

- **Type:** Neural Network (MLPClassifier)
- **Accuracy:** 70% test, 77.5% training
- **Features:** Temperature, Humidity, Pressure, Wind Speed
- **Output:** Yes (Rain) or No (No Rain)

---

## 🔌 API Response Example

```json
{
  "success": true,
  "prediction": "Yes",
  "confidence": 85.3,
  "probabilities": {
    "no_rain": 14.7,
    "rain": 85.3
  }
}
```

---

## 🌐 Full Documentation

For more details, see:
- `FLASK_README.md` - Usage guide
- `FLASK_DEPLOYMENT_GUIDE.md` - Production deployment
- `FLASK_APP_SUMMARY.md` - Project overview

---

## ✨ Next Steps

1. ✅ Start Flask app
2. ✅ Open http://localhost:5000/
3. ✅ Make predictions
4. ✅ Test API endpoints
5. ✅ Read full documentation
6. ✅ Deploy to production (optional)

---

## 🎉 Ready to Go!

Your Flask web application is **production-ready** and includes:
- ✓ Fully trained ML model
- ✓ Beautiful, responsive UI
- ✓ Complete API endpoints
- ✓ Input validation
- ✓ Error handling
- ✓ Comprehensive documentation

**Start making predictions now!** 🌧️

---

**Questions?** Check FLASK_README.md or FLASK_DEPLOYMENT_GUIDE.md

**Last Updated:** March 19, 2026
