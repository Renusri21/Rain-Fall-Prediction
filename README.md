# Rainfall Prediction Using Deep Learning

A complete TensorFlow/Keras deep learning project for predicting rainfall based on meteorological features.

## Project Overview

This project implements an Artificial Neural Network (ANN) using TensorFlow/Keras to classify whether rainfall will occur based on:
- Temperature
- Humidity
- Air Pressure
- Wind Speed

## Project Structure

```
RainfallPredictionProject/
├── rainfall_prediction.py      # Main Python script
├── rainfall_data.csv           # Sample dataset
├── rainfall_model.h5           # Trained model (generated after running)
├── scaler.pkl                  # StandardScaler (generated after running)
├── label_encoder.pkl           # LabelEncoder (generated after running)
├── rainfall_prediction_analysis.png  # Visualizations (generated after running)
└── README.md                   # This file
```

## Requirements

### Python Version
- Python 3.7 or higher

### Required Libraries
```bash
pip install numpy pandas matplotlib seaborn scikit-learn tensorflow
```

## Installation Steps

1. **Clone/Download the project**
   ```bash
   cd C:\RainfallPredictionProject
   ```

2. **Install required packages**
   ```bash
   pip install numpy pandas matplotlib seaborn scikit-learn tensorflow
   ```

3. **Verify TensorFlow installation**
   ```bash
   python -c "import tensorflow; print(f'TensorFlow version: {tensorflow.__version__}')"
   ```

## Running the Project

1. **Navigate to project directory**
   ```bash
   cd C:\RainfallPredictionProject
   ```

2. **Run the script**
   ```bash
   python rainfall_prediction.py
   ```

3. **Script will:**
   - Load and preprocess the rainfall dataset
   - Build and train the neural network
   - Evaluate model performance
   - Display visualizations
   - Make predictions on sample data
   - Save the trained model and utilities

## Model Architecture

```
Input Layer (4 features)
    ↓
Dense Layer (64 neurons, ReLU activation)
    ↓
Dropout (0.3)
    ↓
Dense Layer (32 neurons, ReLU activation)
    ↓
Dropout (0.3)
    ↓
Output Layer (1 neuron, Sigmoid activation)
    ↓
Binary Classification (Yes/No)
```

## Model Specifications

| Parameter | Value |
|-----------|-------|
| Loss Function | Binary Crossentropy |
| Optimizer | Adam |
| Metrics | Accuracy |
| Epochs | 20 |
| Batch Size | 32 |
| Train-Test Split | 80-20 |
| Validation Split | 20% of training data |

## Output Files Generated

1. **rainfall_model.h5** - Saved trained model
2. **scaler.pkl** - Feature scaler for preprocessing
3. **label_encoder.pkl** - Encoder for target variable
4. **rainfall_prediction_analysis.png** - Four visualizations:
   - Training vs Validation Accuracy
   - Training vs Validation Loss
   - Confusion Matrix
   - Model Performance Metrics

## Dataset Format

The `rainfall_data.csv` file contains the following columns:

| Column | Description | Type |
|--------|-------------|------|
| Temperature | Temperature in °C | Numeric |
| Humidity | Humidity percentage | Numeric |
| AirPressure | Atmospheric pressure in hPa | Numeric |
| WindSpeed | Wind speed in km/h | Numeric |
| Precipitation | Target: Yes/No | Categorical |

## Output Format

The script provides comprehensive output including:
- Dataset summary and statistics
- Preprocessing steps
- Model architecture
- Training progress (loss and accuracy per epoch)
- Test accuracy and loss
- Confusion matrix
- Classification report (Precision, Recall, F1-Score)
- Visualizations (saved as PNG)
- Sample prediction result

## Code Features

✅ Clean and well-structured code with proper comments
✅ Handle missing values properly
✅ Feature scaling with StandardScaler
✅ Binary target encoding with LabelEncoder
✅ Train-test split (80-20)
✅ Dropout for regularization
✅ Training history tracking
✅ Comprehensive evaluation metrics
✅ Multiple visualization plots
✅ Predictions on new data
✅ Model persistence (H5 format)
✅ Error handling and warnings suppression

## Using the Saved Model

To use the trained model for predictions later:

```python
import pickle
from tensorflow.keras.models import load_model

# Load model and utilities
model = load_model('rainfall_model.h5')

with open('scaler.pkl', 'rb') as f:
    scaler = pickle.load(f)

with open('label_encoder.pkl', 'rb') as f:
    label_encoder = pickle.load(f)

# Make prediction
new_data = [[28.0, 70, 1012.0, 9.0]]  # [Temperature, Humidity, AirPressure, WindSpeed]
new_data_scaled = scaler.transform(new_data)
prediction = model.predict(new_data_scaled)
result = 'Rainfall' if prediction > 0.5 else 'No Rainfall'
print(f"Prediction: {result}")
```

## Troubleshooting

### Issue: ModuleNotFoundError
**Solution:** Ensure all required packages are installed
```bash
pip install --upgrade numpy pandas matplotlib seaborn scikit-learn tensorflow
```

### Issue: CUDA/GPU errors with TensorFlow
**Solution:** TensorFlow will work on CPU by default. GPU support requires CUDA/cuDNN setup.

### Issue: CSV file not found
**Solution:** Ensure `rainfall_data.csv` is in the same directory as `rainfall_prediction.py`

## Expected Output

The script will display:
- Dataset shape and first 5 rows
- Null values summary
- Feature scaling confirmation
- Model architecture summary
- Training progress for 20 epochs
- Test accuracy (typically 80-95%)
- Confusion matrix
- Classification metrics
- Prediction on sample data

## Performance Notes

- The model trains on sample data (50 records)
- For production use, use a larger, real-world dataset
- Model may require hyperparameter tuning for different datasets
- Performance metrics will vary depending on data distribution

## License

This project is created for educational purposes.

## Author

Created as a comprehensive Deep Learning learning project using TensorFlow/Keras.

---

For more information about TensorFlow/Keras, visit: https://www.tensorflow.org/
