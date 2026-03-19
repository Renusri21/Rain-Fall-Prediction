"""
RAINFALL PREDICTION - REST API
Flask web service for model inference

Usage:
    python flask_api.py
    
Then visit: http://localhost:5000/api/predict
Or POST to: http://localhost:5000/api/predict
"""

from flask import Flask, request, jsonify, render_template_string
import pickle
import pandas as pd
import json
from datetime import datetime
import traceback

app = Flask(__name__)

# Load model and utilities once
try:
    with open('rainfall_model.pkl', 'rb') as f:
        model = pickle.load(f)
    with open('scaler.pkl', 'rb') as f:
        scaler = pickle.load(f)
    with open('label_encoder.pkl', 'rb') as f:
        label_encoder = pickle.load(f)
    print("✓ Model loaded successfully")
except Exception as e:
    print(f"✗ Error loading model: {e}")
    model = scaler = label_encoder = None

# Global variables for tracking
predictions_history = []

# HTML Template for web interface
HTML_TEMPLATE = '''
<!DOCTYPE html>
<html>
<head>
    <title>Rainfall Prediction API</title>
    <style>
        body { font-family: Arial; margin: 40px; background: #f5f5f5; }
        .container { background: white; padding: 20px; border-radius: 8px; max-width: 600px; }
        h1 { color: #333; }
        .form-group { margin: 15px 0; }
        label { display: block; font-weight: bold; margin-bottom: 5px; }
        input { width: 100%; padding: 8px; border: 1px solid #ddd; border-radius: 4px; }
        button { background: #007bff; color: white; padding: 10px 20px; border: none; border-radius: 4px; cursor: pointer; margin-top: 10px; }
        button:hover { background: #0056b3; }
        .result { margin-top: 20px; padding: 15px; background: #f9f9f9; border-left: 4px solid #007bff; }
        .success { border-left-color: #28a745; color: #155724; }
        .error { border-left-color: #dc3545; color: #721c24; }
        .info { font-size: 12px; color: #666; margin-top: 10px; }
        table { width: 100%; border-collapse: collapse; margin-top: 10px; }
        th, td { padding: 10px; text-align: left; border-bottom: 1px solid #ddd; }
        th { background: #f0f0f0; font-weight: bold; }
    </style>
</head>
<body>
    <div class="container">
        <h1>🌧️ Rainfall Prediction API</h1>
        <p>Enter meteorological data to predict rainfall probability</p>
        
        <form id="predictionForm">
            <div class="form-group">
                <label for="temp">Temperature (°C):</label>
                <input type="number" id="temp" name="temperature" step="0.1" value="28.0" required>
            </div>
            <div class="form-group">
                <label for="humidity">Humidity (%):</label>
                <input type="number" id="humidity" name="humidity" min="0" max="100" value="70" required>
            </div>
            <div class="form-group">
                <label for="pressure">Air Pressure (hPa):</label>
                <input type="number" id="pressure" name="pressure" step="0.1" value="1012.0" required>
            </div>
            <div class="form-group">
                <label for="wind">Wind Speed (km/h):</label>
                <input type="number" id="wind" name="wind_speed" step="0.1" value="9.0" required>
            </div>
            <button type="submit">Predict</button>
        </form>
        
        <div id="resultContainer"></div>
        
        <h2>API Examples</h2>
        <p><strong>GET Example:</strong></p>
        <code>/api/predict?temperature=28.0&humidity=70&pressure=1012.0&wind_speed=9.0</code>
        
        <p><strong>POST Example (JSON):</strong></p>
        <pre>
curl -X POST http://localhost:5000/api/predict \\
  -H "Content-Type: application/json" \\
  -d '{
    "temperature": 28.0,
    "humidity": 70,
    "pressure": 1012.0,
    "wind_speed": 9.0
  }'
        </pre>
    </div>
    
    <script>
        document.getElementById('predictionForm').addEventListener('submit', function(e) {
            e.preventDefault();
            const formData = new FormData(this);
            const data = Object.fromEntries(formData);
            
            fetch('/api/predict', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(data)
            })
            .then(r => r.json())
            .then(result => {
                const container = document.getElementById('resultContainer');
                if (result.success) {
                    container.innerHTML = `
                        <div class="result success">
                            <h3>✓ Prediction Result</h3>
                            <p><strong>Prediction:</strong> ${result.prediction}</p>
                            <p><strong>Confidence:</strong> ${result.confidence.toFixed(2)}%</p>
                            <table>
                                <tr>
                                    <th>Scenario</th>
                                    <th>Probability</th>
                                </tr>
                                <tr>
                                    <td>No Rain</td>
                                    <td>${result.probabilities.no_rain.toFixed(2)}%</td>
                                </tr>
                                <tr>
                                    <td>Rain</td>
                                    <td>${result.probabilities.rain.toFixed(2)}%</td>
                                </tr>
                            </table>
                            <p class="info">Processed at: ${new Date(result.timestamp).toLocaleString()}</p>
                        </div>
                    `;
                } else {
                    container.innerHTML = `
                        <div class="result error">
                            <h3>✗ Error</h3>
                            <p>${result.error}</p>
                        </div>
                    `;
                }
            })
            .catch(e => {
                document.getElementById('resultContainer').innerHTML = `
                    <div class="result error">
                        <h3>✗ Network Error</h3>
                        <p>${e.message}</p>
                    </div>
                `;
            });
        });
    </script>
</body>
</html>
'''

@app.route('/', methods=['GET'])
def home():
    """Web interface for predictions"""
    return render_template_string(HTML_TEMPLATE)

@app.route('/api/predict', methods=['GET', 'POST'])
def predict():
    """Predict rainfall for given weather conditions"""
    try:
        if model is None or scaler is None or label_encoder is None:
            return jsonify({
                'success': False,
                'error': 'Model not loaded. Place model files in project directory.'
            }), 500
        
        # Get input data
        if request.method == 'POST':
            data = request.get_json()
        else:
            data = request.args.to_dict()
        
        # Validate required fields
        required_fields = ['temperature', 'humidity', 'pressure', 'wind_speed']
        missing = [f for f in required_fields if f not in data]
        if missing:
            return jsonify({
                'success': False,
                'error': f'Missing required fields: {", ".join(missing)}'
            }), 400
        
        # Convert to float
        try:
            temp = float(data['temperature'])
            humidity = float(data['humidity'])
            pressure = float(data['pressure'])
            wind = float(data['wind_speed'])
        except ValueError as e:
            return jsonify({
                'success': False,
                'error': f'Invalid numeric value: {str(e)}'
            }), 400
        
        # Validate ranges
        if not (0 <= humidity <= 100):
            return jsonify({'success': False, 'error': 'Humidity must be 0-100%'}), 400
        if pressure < 800 or pressure > 1100:
            return jsonify({'success': False, 'error': 'Pressure out of realistic range (800-1100)'}), 400
        if temp < -50 or temp > 60:
            return jsonify({'success': False, 'error': 'Temperature out of realistic range'}), 400
        if wind < 0 or wind > 100:
            return jsonify({'success': False, 'error': 'Wind speed out of realistic range'}), 400
        
        # Make prediction
        input_data = pd.DataFrame([[temp, humidity, pressure, wind]], 
                                  columns=['Temperature', 'Humidity', 'AirPressure', 'WindSpeed'])
        scaled = scaler.transform(input_data)
        prediction = model.predict(scaled)[0]
        probabilities = model.predict_proba(scaled)[0]
        
        # Decode prediction
        result_label = label_encoder.classes_[prediction]
        confidence = float(max(probabilities) * 100)
        
        # Log prediction
        log_entry = {
            'timestamp': datetime.now().isoformat(),
            'input': {
                'temperature': temp,
                'humidity': humidity,
                'pressure': pressure,
                'wind_speed': wind
            },
            'prediction': result_label,
            'confidence': confidence
        }
        predictions_history.append(log_entry)
        
        return jsonify({
            'success': True,
            'prediction': result_label,
            'confidence': confidence,
            'probabilities': {
                'no_rain': float(probabilities[0] * 100),
                'rain': float(probabilities[1] * 100)
            },
            'timestamp': datetime.now().isoformat(),
            'input': {
                'temperature': temp,
                'humidity': humidity,
                'pressure': pressure,
                'wind_speed': wind
            }
        })
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Server error: {str(e)}'
        }), 500

@app.route('/api/batch-predict', methods=['POST'])
def batch_predict():
    """Predict rainfall for multiple weather conditions"""
    try:
        if model is None or scaler is None or label_encoder is None:
            return jsonify({
                'success': False,
                'error': 'Model not loaded'
            }), 500
        
        data = request.get_json()
        
        if not isinstance(data, list):
            return jsonify({
                'success': False,
                'error': 'Expected JSON array of weather records'
            }), 400
        
        results = []
        for idx, record in enumerate(data):
            try:
                required_fields = ['temperature', 'humidity', 'pressure', 'wind_speed']
                if not all(f in record for f in required_fields):
                    results.append({'error': f'Record {idx}: Missing required fields'})
                    continue
                
                temp = float(record['temperature'])
                humidity = float(record['humidity'])
                pressure = float(record['pressure'])
                wind = float(record['wind_speed'])
                
                input_data = pd.DataFrame([[temp, humidity, pressure, wind]], 
                                        columns=['Temperature', 'Humidity', 'AirPressure', 'WindSpeed'])
                scaled = scaler.transform(input_data)
                prediction = model.predict(scaled)[0]
                probabilities = model.predict_proba(scaled)[0]
                
                result_label = label_encoder.classes_[prediction]
                
                results.append({
                    'prediction': result_label,
                    'confidence': float(max(probabilities) * 100),
                    'probabilities': {
                        'no_rain': float(probabilities[0] * 100),
                        'rain': float(probabilities[1] * 100)
                    }
                })
            except Exception as e:
                results.append({'error': f'Record {idx}: {str(e)}'})
        
        return jsonify({
            'success': True,
            'total_records': len(data),
            'predictions': results
        })
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/history', methods=['GET'])
def get_history():
    """Get prediction history"""
    limit = request.args.get('limit', 100, type=int)
    return jsonify({
        'total_predictions': len(predictions_history),
        'recent_predictions': predictions_history[-limit:]
    })

@app.route('/api/stats', methods=['GET'])
def get_stats():
    """Get prediction statistics"""
    if not predictions_history:
        return jsonify({
            'total_predictions': 0,
            'rain_predictions': 0,
            'no_rain_predictions': 0
        })
    
    rain_count = sum(1 for p in predictions_history if p['prediction'] == 'Yes')
    no_rain_count = len(predictions_history) - rain_count
    
    return jsonify({
        'total_predictions': len(predictions_history),
        'rain_predictions': rain_count,
        'no_rain_predictions': no_rain_count,
        'rain_percentage': (rain_count / len(predictions_history) * 100) if predictions_history else 0
    })

@app.route('/api/health', methods=['GET'])
def health():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy' if model is not None else 'unhealthy',
        'model_loaded': model is not None,
        'timestamp': datetime.now().isoformat()
    })

if __name__ == '__main__':
    print("""
    ╔════════════════════════════════════════════════╗
    ║   🌧️  RAINFALL PREDICTION API - RUNNING      ║
    ╚════════════════════════════════════════════════╝
    
    🌐 Web Interface: http://localhost:5000/
    📊 API Endpoints:
       - GET  /api/predict?temperature=28&humidity=70&pressure=1012&wind_speed=9
       - POST /api/predict (JSON body)
       - POST /api/batch-predict (JSON array)
       - GET  /api/history?limit=50
       - GET  /api/stats
       - GET  /api/health
    
    💡 Example cURL:
       curl "http://localhost:5000/api/predict?temperature=28&humidity=70&pressure=1012&wind_speed=9"
    
    Press CTRL+C to stop server
    """)
    
    app.run(debug=False, host='0.0.0.0', port=5000)
