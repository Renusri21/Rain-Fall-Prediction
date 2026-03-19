"""
Flask Web Application - Rainfall Prediction System
====================================================
A complete Flask application for rainfall prediction using a trained machine learning model.

Features:
    - Load pre-trained neural network model
    - Web interface for predictions
    - REST API endpoint for predictions
    - Input validation and error handling
    - Real-time prediction results

Author: AI Assistant
Date: March 19, 2026
Version: 1.0
"""

from flask import Flask, render_template, request, jsonify
import pickle
import pandas as pd
import numpy as np
import os
from datetime import datetime

# ============================================================================
# DETERMINE PROJECT DIRECTORY
# ============================================================================
# Get the directory where this script is located
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
os.chdir(SCRIPT_DIR)  # Change working directory to script location

# ============================================================================
# INITIALIZE FLASK APP
# ============================================================================
app = Flask(__name__, template_folder='templates', static_folder='static')
app.config['JSON_SORT_KEYS'] = False

# ============================================================================
# GLOBAL VARIABLES FOR MODEL AND UTILITIES
# ============================================================================
model = None
scaler = None
label_encoder = None
model_loaded = False

# ============================================================================
# LOAD MODEL AND UTILITIES ON APP STARTUP
# ============================================================================
def load_model():
    """
    Load the trained machine learning model and utility files (scaler, encoder).
    Called once when the Flask app starts.
    
    Returns:
        bool: True if all files loaded successfully, False otherwise
    """
    global model, scaler, label_encoder, model_loaded
    
    try:
        print("\n" + "="*70)
        print("LOADING MACHINE LEARNING MODEL AND UTILITIES")
        print("="*70)
        
        # List of required files
        required_files = ['rainfall_model.pkl', 'scaler.pkl', 'label_encoder.pkl']
        missing_files = []
        
        # Check if all required files exist
        for file in required_files:
            if not os.path.exists(file):
                missing_files.append(file)
        
        if missing_files:
            print(f"\n❌ ERROR: Missing required files:")
            for file in missing_files:
                print(f"   - {file}")
            print("\nPlease ensure these files are in the project directory:")
            print("   1. Train the model: python rainfall_prediction_sklearn.py")
            return False
        
        # Load the trained model
        print("\n[1] Loading trained model...")
        with open('rainfall_model.pkl', 'rb') as f:
            model = pickle.load(f)
        print("✓ Model loaded successfully")
        print(f"  Model type: {type(model).__name__}")
        
        # Load the feature scaler
        print("\n[2] Loading feature scaler...")
        with open('scaler.pkl', 'rb') as f:
            scaler = pickle.load(f)
        print("✓ Scaler loaded successfully")
        
        # Load the label encoder
        print("\n[3] Loading label encoder...")
        with open('label_encoder.pkl', 'rb') as f:
            label_encoder = pickle.load(f)
        print("✓ Label encoder loaded successfully")
        print(f"  Classes: {list(label_encoder.classes_)}")
        
        model_loaded = True
        print("\n" + "="*70)
        print("✓ ALL MODELS LOADED SUCCESSFULLY")
        print("="*70 + "\n")
        
        return True
        
    except FileNotFoundError as e:
        print(f"\n❌ ERROR: File not found - {str(e)}")
        return False
    except Exception as e:
        print(f"\n❌ ERROR: Failed to load model - {str(e)}")
        return False

# ============================================================================
# ROUTE: HOME PAGE
# ============================================================================
@app.route('/', methods=['GET'])
def home():
    """
    Display the home page with the rainfall prediction form.
    
    Returns:
        Rendered HTML template (index.html)
    """
    return render_template('index.html')

# ============================================================================
# ROUTE: PREDICT
# ============================================================================
@app.route('/predict', methods=['POST'])
def predict():
    """
    Handle prediction requests from the web form or API.
    
    Expected JSON body:
    {
        "temperature": float,
        "humidity": float,
        "pressure": float,
        "wind_speed": float
    }
    
    Returns:
        JSON response with prediction and confidence
    """
    try:
        # Check if model is loaded
        if not model_loaded or model is None or scaler is None or label_encoder is None:
            print("ERROR: Model or utilities not loaded")
            print(f"model_loaded={model_loaded}, model={model}, scaler={scaler}, label_encoder={label_encoder}")
            return jsonify({
                'error': 'Model not loaded. Please ensure all model files are present.',
                'success': False
            }), 500
        
        # Get JSON data from request
        data = request.get_json(silent=True, force=True)
        
        if not data:
            print("ERROR: No JSON data received")
            return jsonify({
                'error': 'No data provided. Please submit weather data.',
                'success': False
            }), 400
        
        # Extract input values
        try:
            temperature = float(data.get('temperature'))
            humidity = float(data.get('humidity'))
            pressure = float(data.get('pressure'))
            wind_speed = float(data.get('wind_speed'))
        except (TypeError, ValueError):
            return jsonify({
                'error': 'Invalid input values. Please provide valid numbers.',
                'success': False
            }), 400
        
        # Validate input ranges
        if not (-50 <= temperature <= 60):
            return jsonify({
                'error': 'Temperature must be between -50°C and 60°C',
                'success': False
            }), 400
        
        if not (0 <= humidity <= 100):
            return jsonify({
                'error': 'Humidity must be between 0% and 100%',
                'success': False
            }), 400
        
        if not (800 <= pressure <= 1100):
            return jsonify({
                'error': 'Pressure must be between 800 and 1100 hPa',
                'success': False
            }), 400
        
        if not (0 <= wind_speed <= 100):
            return jsonify({
                'error': 'Wind speed must be between 0 and 100 km/h',
                'success': False
            }), 400
        
        # Prepare input data for model
        input_data = pd.DataFrame([[temperature, humidity, pressure, wind_speed]], 
                                  columns=['Temperature', 'Humidity', 'AirPressure', 'WindSpeed'])
        
        # Scale the input data using the fitted scaler
        scaled_input = scaler.transform(input_data)
        
        # Make prediction with the model
        prediction_class = model.predict(scaled_input)[0]
        prediction_probabilities = model.predict_proba(scaled_input)[0]
        
        # Decode prediction to readable format
        predicted_label = label_encoder.classes_[prediction_class]
        
        # Calculate confidence (highest probability)
        confidence = float(max(prediction_probabilities) * 100)
        
        # Prepare response data
        response = {
            'success': True,
            'prediction': predicted_label,
            'confidence': confidence,
            'probabilities': {
                'no_rain': float(prediction_probabilities[0] * 100),
                'rain': float(prediction_probabilities[1] * 100)
            },
            'input': {
                'temperature': temperature,
                'humidity': humidity,
                'pressure': pressure,
                'wind_speed': wind_speed
            },
            'timestamp': datetime.now().isoformat(),
            'model_info': {
                'name': 'MLPClassifier (Scikit-learn)',
                'accuracy': '70%',
                'features': ['Temperature', 'Humidity', 'Air Pressure', 'Wind Speed']
            }
        }
        
        return jsonify(response), 200
        
    except Exception as e:
        import traceback
        error_trace = traceback.format_exc()
        print(f"\n❌ ERROR in /predict endpoint:")
        print(error_trace)
        return jsonify({
            'error': f'Prediction failed: {str(e)}',
            'success': False,
            'error_type': type(e).__name__
        }), 500

# ============================================================================
# ROUTE: DEBUG STATUS
# ============================================================================
@app.route('/api/debug', methods=['GET'])
def debug_status():
    """Debug endpoint to check if models are loaded properly"""
    global model, scaler, label_encoder, model_loaded
    
    return jsonify({
        'model_loaded': model_loaded,
        'model_is_none': model is None,
        'scaler_is_none': scaler is None,
        'label_encoder_is_none': label_encoder is None,
        'model_type': str(type(model)) if model else 'None',
        'scaler_type': str(type(scaler)) if scaler else 'None',
        'label_encoder_type': str(type(label_encoder)) if label_encoder else 'None'
    }), 200

# ============================================================================
# ROUTE: MODEL INFO (API)
# ============================================================================
@app.route('/api/model-info', methods=['GET'])
def model_info():
    """
    Return information about the machine learning model.
    
    Returns:
        JSON response with model details
    """
    if not model_loaded:
        return jsonify({
            'error': 'Model not loaded',
            'model_loaded': False
        }), 500
    
    return jsonify({
        'model_loaded': True,
        'model_type': type(model).__name__,
        'model_name': 'Rainfall Prediction Neural Network',
        'framework': 'scikit-learn',
        'test_accuracy': '70%',
        'training_accuracy': '77.5%',
        'convergence': '27 epochs',
        'training_time': '0.03 seconds',
        'features': ['Temperature (°C)', 'Humidity (%)', 'Air Pressure (hPa)', 'Wind Speed (km/h)'],
        'output_classes': list(label_encoder.classes_),
        'version': '1.0',
        'created': 'March 18, 2026'
    }), 200

# ============================================================================
# ROUTE: HEALTH CHECK (API)
# ============================================================================
@app.route('/api/health', methods=['GET'])
def health():
    """
    Check if the Flask application and model are running properly.
    
    Returns:
        JSON response with health status
    """
    return jsonify({
        'status': 'healthy' if model_loaded else 'unhealthy',
        'model_loaded': model_loaded,
        'timestamp': datetime.now().isoformat()
    }), 200

# ============================================================================
# ERROR HANDLERS
# ============================================================================
@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors"""
    return jsonify({'error': 'Endpoint not found', 'status': 404}), 404

@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors"""
    return jsonify({'error': 'Internal server error', 'status': 500}), 500

# ============================================================================
# MAIN APPLICATION ENTRY POINT
# ============================================================================
if __name__ == '__main__':
    print("\n")
    print("╔" + "="*68 + "╗")
    print("║" + " "*68 + "║")
    print("║" + "  🌧️  RAINFALL PREDICTION SYSTEM - FLASK WEB APPLICATION  🌧️  ".center(68) + "║")
    print("║" + " "*68 + "║")
    print("╚" + "="*68 + "╝")
    
    # Load model before starting the app
    if not load_model():
        print("\n❌ FATAL ERROR: Could not load the machine learning model.")
        print("Please ensure the model files exist in the project directory:")
        print("  - rainfall_model.pkl")
        print("  - scaler.pkl")
        print("  - label_encoder.pkl")
        print("\nTo generate these files, run:")
        print("  python rainfall_prediction_sklearn.py")
        exit(1)
    
    # Start the Flask development server
    print("🚀 STARTING FLASK APPLICATION...")
    print("\n" + "="*70)
    print("📍 Web Interface: http://localhost:5000/")
    print("📍 API Endpoint:  http://localhost:5000/predict")
    print("📍 Health Check:  http://localhost:5000/api/health")
    print("📍 Model Info:    http://localhost:5000/api/model-info")
    print("="*70)
    print("\n✓ Application is running!")
    print("✓ Press CTRL+C to stop the server\n")
    
    # Get port from environment variable (for cloud deployment) or default to 5000
    port = int(os.environ.get('PORT', 5000))
    
    # Run Flask app on localhost:5000 (or PORT for cloud deployments)
    # Set debug=True for development (auto-reload on file changes)
    # Set debug=False for production (more secure)
    app.run(
        host='0.0.0.0',           # Listen on all network interfaces
        port=port,                 # Port number (from env or default 5000)
        debug=False,               # Disable debug mode for production
        use_reloader=False         # Disable auto-reloader
    )
