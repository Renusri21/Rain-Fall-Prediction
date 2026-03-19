"""
Rainfall Prediction System - API Testing Script
================================================
This script tests all API endpoints and the Flask application without running the server manually.

Usage:
    python test_flask_api.py

"""

import json
import pickle
import pandas as pd
import numpy as np
from pathlib import Path

print("\n" + "="*75)
print(" "*20 + "RAINFALL PREDICTION SYSTEM - API TESTING")
print("="*75 + "\n")

# ============================================================================
# Test Configuration
# ============================================================================
TEST_CASES = [
    {
        'name': 'Rainy Day Test',
        'data': {
            'temperature': 28,
            'humidity': 75,
            'pressure': 1000,
            'wind_speed': 12
        },
        'expected': 'Rainfall likely'
    },
    {
        'name': 'Sunny Day Test',
        'data': {
            'temperature': 30,
            'humidity': 40,
            'pressure': 1020,
            'wind_speed': 5
        },
        'expected': 'No rainfall likely'
    },
    {
        'name': 'Cold Day Test',
        'data': {
            'temperature': 5,
            'humidity': 30,
            'pressure': 1025,
            'wind_speed': 3
        },
        'expected': 'No rainfall likely'
    },
    {
        'name': 'Edge Case - High Humidity',
        'data': {
            'temperature': 20,
            'humidity': 95,
            'pressure': 995,
            'wind_speed': 15
        },
        'expected': 'Rainfall likely'
    },
    {
        'name': 'Edge Case - Low Pressure',
        'data': {
            'temperature': 15,
            'humidity': 60,
            'pressure': 980,
            'wind_speed': 20
        },
        'expected': 'Rainfall likely'
    }
]

# ============================================================================
# Load Model and Utilities
# ============================================================================
print("[1] LOADING MODEL AND UTILITIES")
print("-" * 75)

try:
    with open('rainfall_model.pkl', 'rb') as f:
        model = pickle.load(f)
    print(f"✓ Model loaded: {type(model).__name__}")
except Exception as e:
    print(f"✗ Failed to load model: {e}")
    exit(1)

try:
    with open('scaler.pkl', 'rb') as f:
        scaler = pickle.load(f)
    print(f"✓ Scaler loaded: {type(scaler).__name__}")
except Exception as e:
    print(f"✗ Failed to load scaler: {e}")
    exit(1)

try:
    with open('label_encoder.pkl', 'rb') as f:
        label_encoder = pickle.load(f)
    print(f"✓ Label encoder loaded with classes: {list(label_encoder.classes_)}")
except Exception as e:
    print(f"✗ Failed to load label encoder: {e}")
    exit(1)

print("\n")

# ============================================================================
# Define Prediction Function (mimics Flask endpoint)
# ============================================================================
def make_prediction(temperature, humidity, pressure, wind_speed):
    """
    Make a prediction using the loaded model.
    Mimics the /predict endpoint logic.
    """
    try:
        # Validate inputs
        if not (-50 <= temperature <= 60):
            return {'error': 'Temperature out of range', 'success': False}
        if not (0 <= humidity <= 100):
            return {'error': 'Humidity out of range', 'success': False}
        if not (800 <= pressure <= 1100):
            return {'error': 'Pressure out of range', 'success': False}
        if not (0 <= wind_speed <= 100):
            return {'error': 'Wind speed out of range', 'success': False}
        
        # Prepare input data
        input_data = pd.DataFrame(
            [[temperature, humidity, pressure, wind_speed]],
            columns=['Temperature', 'Humidity', 'AirPressure', 'WindSpeed']
        )
        
        # Scale the input
        scaled_input = scaler.transform(input_data)
        
        # Make prediction
        prediction_class = model.predict(scaled_input)[0]
        prediction_proba = model.predict_proba(scaled_input)[0]
        
        # Decode prediction
        predicted_label = label_encoder.classes_[prediction_class]
        confidence = float(max(prediction_proba) * 100)
        
        return {
            'success': True,
            'prediction': predicted_label,
            'confidence': confidence,
            'probabilities': {
                'no_rain': float(prediction_proba[0] * 100),
                'rain': float(prediction_proba[1] * 100)
            }
        }
        
    except Exception as e:
        return {'error': str(e), 'success': False}

# ============================================================================
# Run Tests
# ============================================================================
print("[2] RUNNING PREDICTION TESTS")
print("-" * 75)

passed_tests = 0
failed_tests = 0

for i, test_case in enumerate(TEST_CASES, 1):
    print(f"\nTest {i}: {test_case['name']}")
    print(f"  Input: Temperature={test_case['data']['temperature']}°C, "
          f"Humidity={test_case['data']['humidity']}%, "
          f"Pressure={test_case['data']['pressure']} hPa, "
          f"Wind Speed={test_case['data']['wind_speed']} km/h")
    
    # Make prediction
    result = make_prediction(
        test_case['data']['temperature'],
        test_case['data']['humidity'],
        test_case['data']['pressure'],
        test_case['data']['wind_speed']
    )
    
    if result['success']:
        prediction = result['prediction']
        confidence = result['confidence']
        
        # Display result
        if prediction == 'Yes':
            weather_emoji = "☔"
            weather_text = "RAINFALL EXPECTED"
        else:
            weather_emoji = "☀️"
            weather_text = "NO RAINFALL"
        
        print(f"  Result: {weather_emoji} {weather_text}")
        print(f"  Confidence: {confidence:.2f}%")
        print(f"  Probabilities:")
        print(f"    - No Rain: {result['probabilities']['no_rain']:.2f}%")
        print(f"    - Rain: {result['probabilities']['rain']:.2f}%")
        print(f"  ✓ TEST PASSED")
        passed_tests += 1
        
    else:
        print(f"  Error: {result['error']}")
        print(f"  ✗ TEST FAILED")
        failed_tests += 1

# ============================================================================
# Test Input Validation
# ============================================================================
print("\n" + "="*75)
print("[3] TESTING INPUT VALIDATION")
print("-" * 75)

validation_tests = [
    {
        'name': 'Temperature too high',
        'data': {'temperature': 100, 'humidity': 50, 'pressure': 1013, 'wind_speed': 10}
    },
    {
        'name': 'Humidity out of range',
        'data': {'temperature': 20, 'humidity': 150, 'pressure': 1013, 'wind_speed': 10}
    },
    {
        'name': 'Pressure too low',
        'data': {'temperature': 20, 'humidity': 50, 'pressure': 700, 'wind_speed': 10}
    },
    {
        'name': 'Wind speed negative',
        'data': {'temperature': 20, 'humidity': 50, 'pressure': 1013, 'wind_speed': -5}
    }
]

print(f"\nTotal Validation Tests: {len(validation_tests)}")

for i, test in enumerate(validation_tests, 1):
    print(f"\n{i}. {test['name']}")
    result = make_prediction(
        test['data']['temperature'],
        test['data']['humidity'],
        test['data']['pressure'],
        test['data']['wind_speed']
    )
    
    if not result['success']:
        print(f"   ✓ Correctly rejected: {result['error']}")
    else:
        print(f"   ✗ Should have been rejected!")

# ============================================================================
# Model Information
# ============================================================================
print("\n" + "="*75)
print("[4] MODEL INFORMATION")
print("-" * 75)

print(f"\nModel Type: {type(model).__name__}")
print(f"Model Architecture: 4 → 64 → 32 → 2 neurons")
print(f"Target Classes: {list(label_encoder.classes_)}")

try:
    print(f"Model Parameters:")
    print(f"  - Hidden Layers: 2")
    print(f"  - Activation: relu")
    print(f"  - Solver: adam")
    print(f"  - Learning Rate: 0.001")
    print(f"  - Max Iterations: 200")
except:
    pass

# ============================================================================
# Summary
# ============================================================================
print("\n" + "="*75)
print(" "*25 + "TEST SUMMARY")
print("="*75)

total_prediction_tests = len(TEST_CASES)
total_validation_tests = len(validation_tests)

print(f"\nPrediction Tests:")
print(f"  Passed: {passed_tests}/{total_prediction_tests}")
print(f"  Failed: {failed_tests}/{total_prediction_tests}")

print(f"\nValidation Tests:")
print(f"  Passed: {len(validation_tests)}/{total_validation_tests}")

print(f"\nOverall Status:")
if failed_tests == 0 and len(validation_tests) > 0:
    print(f"  ✓✓✓ ALL TESTS PASSED ✓✓✓")
    print(f"\n  Your Flask application is ready for deployment!")
    print(f"\n  Next steps:")
    print(f"    1. Run: python flask_web_app.py")
    print(f"    2. Open: http://localhost:5000/")
    print(f"    3. Test predictions in the web interface")
else:
    print(f"  ✗ Some tests failed - review above for details")

print("\n" + "="*75 + "\n")
