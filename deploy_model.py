# ============================================================================
# MODEL DEPLOYMENT & INFERENCE SCRIPT
# ============================================================================
# This script demonstrates how to load and use the trained model in production
# ============================================================================

import pickle
import numpy as np
import pandas as pd
from datetime import datetime

print("="*70)
print("RAINFALL PREDICTION MODEL - DEPLOYMENT & INFERENCE")
print("="*70)

# ============================================================================
# STEP 1: LOAD TRAINED MODEL AND UTILITIES
# ============================================================================
print("\n[Step 1] Loading Trained Model & Utilities...")

try:
    # Load the trained model
    with open('rainfall_model.pkl', 'rb') as f:
        model = pickle.load(f)
    print("✓ Model loaded successfully")
    
    # Load feature scaler
    with open('scaler.pkl', 'rb') as f:
        scaler = pickle.load(f)
    print("✓ Scaler loaded successfully")
    
    # Load label encoder
    with open('label_encoder.pkl', 'rb') as f:
        label_encoder = pickle.load(f)
    print("✓ Label encoder loaded successfully")
    
except FileNotFoundError as e:
    print(f"✗ Error: {e}")
    print("Make sure model files exist: rainfall_model.pkl, scaler.pkl, label_encoder.pkl")
    exit()

# ============================================================================
# STEP 2: MAKE PREDICTIONS ON NEW DATA
# ============================================================================
print("\n[Step 2] Making Predictions on New Weather Data...")

# Define multiple test cases
test_cases = [
    {
        'name': 'Warm & Humid',
        'data': [28.0, 70, 1012.0, 9.0]  # [Temp, Humidity, Pressure, WindSpeed]
    },
    {
        'name': 'Cool & Dry',
        'data': [25.0, 55, 1014.0, 5.0]
    },
    {
        'name': 'Hot & Windy',
        'data': [32.0, 60, 1010.0, 12.0]
    },
    {
        'name': 'Mild & Calm',
        'data': [27.5, 65, 1013.0, 7.0]
    }
]

print("\n" + "-"*70)
print(f"{'Scenario':<15} | {'Temperature':<12} | {'Humidity':<10} | {'Pressure':<10} | {'Wind':<8} | Prediction")
print("-"*70)

predictions_data = []

for test_case in test_cases:
    scenario = test_case['name']
    raw_data = test_case['data']
    
    # Prepare data for prediction
    feature_names = ['Temperature', 'Humidity', 'AirPressure', 'WindSpeed']
    input_df = pd.DataFrame([raw_data], columns=feature_names)
    
    # Scale the input data
    scaled_data = scaler.transform(input_df)
    
    # Make prediction
    prediction_prob = model.predict_proba(scaled_data)[0]
    prediction = model.predict(scaled_data)[0]
    
    # Get predicted class and confidence
    predicted_class = label_encoder.classes_[prediction]
    confidence = max(prediction_prob) * 100
    
    # Store results
    predictions_data.append({
        'Scenario': scenario,
        'Temperature': raw_data[0],
        'Humidity': raw_data[1],
        'Pressure': raw_data[2],
        'WindSpeed': raw_data[3],
        'Prediction': predicted_class,
        'Confidence': confidence,
        'Prob_No': prediction_prob[0] * 100,
        'Prob_Yes': prediction_prob[1] * 100
    })
    
    # Print result
    print(f"{scenario:<15} | {raw_data[0]:<12.1f} | {raw_data[1]:<10} | {raw_data[2]:<10.1f} | {raw_data[3]:<8.1f} | {predicted_class} ({confidence:.1f}%)")

print("-"*70)

# ============================================================================
# STEP 3: DISPLAY DETAILED PREDICTIONS
# ============================================================================
print("\n[Step 3] Detailed Prediction Results...")
print()

for result in predictions_data:
    print(f"Scenario: {result['Scenario']}")
    print(f"  Temperature: {result['Temperature']}°C")
    print(f"  Humidity: {result['Humidity']}%")
    print(f"  Air Pressure: {result['Pressure']} hPa")
    print(f"  Wind Speed: {result['WindSpeed']} km/h")
    print(f"  ───────────────────────────────────")
    print(f"  Prediction: {result['Prediction'].upper()}")
    print(f"  Confidence: {result['Confidence']:.2f}%")
    print(f"  Probability (No Rain): {result['Prob_No']:.2f}%")
    print(f"  Probability (Rain): {result['Prob_Yes']:.2f}%")
    print()

# ============================================================================
# STEP 4: BATCH PREDICTION
# ============================================================================
print("[Step 4] Batch Prediction Example...")

# Create a batch of predictions
batch_data = pd.DataFrame([
    [28.5, 65, 1013.2, 8.5],
    [26.8, 72, 1011.5, 10.3],
    [30.1, 55, 1014.1, 5.8],
    [27.3, 68, 1012.6, 9.1],
    [25.5, 75, 1010.9, 11.2]
], columns=['Temperature', 'Humidity', 'AirPressure', 'WindSpeed'])

print("\nInput Batch:")
print(batch_data)

# Scale and predict
batch_scaled = scaler.transform(batch_data)
batch_predictions = model.predict(batch_scaled)
batch_probabilities = model.predict_proba(batch_scaled)

# Display batch results
print("\nBatch Predictions:")
print("-"*70)
for i, (pred, probs) in enumerate(zip(batch_predictions, batch_probabilities)):
    predicted_class = label_encoder.classes_[pred]
    confidence = max(probs) * 100
    print(f"Sample {i+1}: {predicted_class} (Confidence: {confidence:.2f}%)")

# ============================================================================
# STEP 5: MODEL INFORMATION
# ============================================================================
print("\n[Step 5] Model Information...")
print()
print(f"Model Type: {type(model).__name__}")
print(f"Model Architecture: Input(4) → Hidden(64) → Hidden(32) → Output(2)")
print(f"Activation: ReLU (hidden), Softmax (output)")
print(f"Solver: adam")
print(f"Training Convergence: 27 iterations")
print(f"Test Accuracy: 70%")
print(f"Training Accuracy: 77.5%")
print(f"Number of Classes: {len(label_encoder.classes_)}")
print(f"Classes: {', '.join(label_encoder.classes_)}")

# ============================================================================
# STEP 6: API-STYLE PREDICTION FUNCTION
# ============================================================================
print("\n[Step 6] API Function for Production Deployment...")
print()

def predict_rainfall(temperature, humidity, air_pressure, wind_speed):
    """
    Production-ready API function for rainfall prediction
    
    Args:
        temperature (float): Temperature in Celsius
        humidity (int): Humidity percentage (0-100)
        air_pressure (float): Atmospheric pressure in hPa
        wind_speed (float): Wind speed in km/h
    
    Returns:
        dict: Prediction result with class and confidence
    """
    # Prepare input
    input_data = pd.DataFrame([
        [temperature, humidity, air_pressure, wind_speed]
    ], columns=['Temperature', 'Humidity', 'AirPressure', 'WindSpeed'])
    
    # Scale
    scaled_input = scaler.transform(input_data)
    
    # Predict
    prediction = model.predict(scaled_input)[0]
    probabilities = model.predict_proba(scaled_input)[0]
    
    # Format result
    result = {
        'timestamp': datetime.now().isoformat(),
        'input': {
            'temperature': temperature,
            'humidity': humidity,
            'air_pressure': air_pressure,
            'wind_speed': wind_speed
        },
        'prediction': label_encoder.classes_[prediction],
        'confidence': float(max(probabilities) * 100),
        'probabilities': {
            'no_rain': float(probabilities[0] * 100),
            'rain': float(probabilities[1] * 100)
        }
    }
    
    return result

# Test the API function
print("Testing API Function:")
print()
api_result = predict_rainfall(temperature=28.0, humidity=70, air_pressure=1012.0, wind_speed=9.0)
print(f"API Result: {api_result}")

# ============================================================================
# STEP 7: SAVE PREDICTIONS TO CSV
# ============================================================================
print("\n[Step 7] Saving Predictions to CSV...")

predictions_df = pd.DataFrame(predictions_data)
predictions_df.to_csv('predictions_results.csv', index=False)
print(f"✓ Predictions saved to 'predictions_results.csv'")

# ============================================================================
# DEPLOYMENT SUMMARY
# ============================================================================
print("\n" + "="*70)
print("DEPLOYMENT SUMMARY")
print("="*70)
print("\n✓ Model loaded and ready for inference")
print("✓ Generated predictions for test scenarios")
print("✓ API function available for production use")
print("✓ Results saved to predictions_results.csv")
print("\nModel Performance:")
print("  - Test Accuracy: 70%")
print("  - Training Accuracy: 77.5%")
print("  - Convergence: 27/100 epochs")
print("\nNext Steps for Production:")
print("  1. Deploy to cloud (AWS, GCP, Azure)")
print("  2. Create REST API endpoint")
print("  3. Monitor predictions and accuracy")
print("  4. Retrain with new data periodically")
print("="*70)
