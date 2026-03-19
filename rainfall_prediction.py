# ============================================================================
# RAINFALL PREDICTION USING DEEP LEARNING (TensorFlow/Keras)
# ============================================================================
# This script predicts rainfall (Yes/No) based on meteorological features
# using an Artificial Neural Network (ANN) build with TensorFlow/Keras
# ============================================================================

# ============================================================================
# STEP 1: IMPORT REQUIRED LIBRARIES
# ============================================================================
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.metrics import confusion_matrix, classification_report, accuracy_score
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout
import warnings

# Suppress warnings for cleaner output
warnings.filterwarnings('ignore')

# Set random seeds for reproducibility
np.random.seed(42)
tf.random.set_seed(42)

print("="*70)
print("RAINFALL PREDICTION USING DEEP LEARNING (TensorFlow/Keras)")
print("="*70)

# ============================================================================
# STEP 2: LOAD DATASET
# ============================================================================
print("\n[Step 1] Loading Dataset...")

# Load CSV file
df = pd.read_csv('rainfall_data.csv')

print(f"Dataset Shape: {df.shape}")
print(f"\nFirst 5 rows of the dataset:")
print(df.head())

print(f"\nDataset Info:")
print(df.info())

print(f"\nNull Values Count:")
print(df.isnull().sum())

print(f"\nDataset Statistics:")
print(df.describe())

# ============================================================================
# STEP 3: DATA PREPROCESSING
# ============================================================================
print("\n[Step 2] Data Preprocessing...")

# 3.1 Handle Missing Values (if any)
print("\nHandling Missing Values...")
df = df.dropna()  # Remove rows with missing values
print(f"Dataset shape after removing null values: {df.shape}")

# 3.2 Separate features and target
print("\nSeparating Features and Target...")
X = df.drop('Precipitation', axis=1)  # Features (all columns except target)
y = df['Precipitation']  # Target variable

print(f"Features shape: {X.shape}")
print(f"Target shape: {y.shape}")
print(f"Feature names: {list(X.columns)}")

# 3.3 Convert categorical target (Yes/No) to numerical (1/0) using LabelEncoder
print("\nEncoding Target Variable...")
label_encoder = LabelEncoder()
y_encoded = label_encoder.fit_transform(y)

# Display encoding mapping
print(f"Encoding mapping: {dict(zip(label_encoder.classes_, label_encoder.transform(label_encoder.classes_)))}")
print(f"Sample of encoded target: {y_encoded[:5]}")

# 3.4 Apply StandardScaler to features
print("\nApplying StandardScaler to Features...")
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

print(f"Features scaled. Shape: {X_scaled.shape}")
print(f"Sample of scaled features (first 2 rows):\n{X_scaled[:2]}")

# 3.5 Split dataset into training and testing sets (80-20 split)
print("\nSplitting Dataset (80% Train, 20% Test)...")
X_train, X_test, y_train, y_test = train_test_split(
    X_scaled,
    y_encoded,
    test_size=0.2,
    random_state=42
)

print(f"X_train shape: {X_train.shape}")
print(f"X_test shape: {X_test.shape}")
print(f"y_train shape: {y_train.shape}")
print(f"y_test shape: {y_test.shape}")

# ============================================================================
# STEP 4: MODEL BUILDING
# ============================================================================
print("\n[Step 3] Building Neural Network Model...")

# Get number of input features
num_features = X_train.shape[1]

# Create Sequential model
model = Sequential([
    Dense(64, activation='relu', input_dim=num_features),     # Input layer with 64 neurons
    Dropout(0.3),                                              # Dropout for regularization
    Dense(32, activation='relu'),                              # Hidden layer with 32 neurons
    Dropout(0.3),                                              # Dropout for regularization
    Dense(1, activation='sigmoid')                             # Output layer for binary classification
])

print("Model Architecture:")
model.summary()

# ============================================================================
# STEP 5: MODEL COMPILATION
# ============================================================================
print("\n[Step 4] Compiling Model...")

model.compile(
    optimizer='adam',
    loss='binary_crossentropy',
    metrics=['accuracy']
)

print("Model compiled successfully!")
print("Optimizer: adam")
print("Loss Function: binary_crossentropy")
print("Metrics: accuracy")

# ============================================================================
# STEP 6: MODEL TRAINING
# ============================================================================
print("\n[Step 5] Training Model...")
print("Training for 20 epochs with batch size 32...")

history = model.fit(
    X_train,
    y_train,
    epochs=20,
    batch_size=32,
    validation_split=0.2,
    verbose=1
)

print("\nModel training completed!")

# ============================================================================
# STEP 7: MODEL EVALUATION
# ============================================================================
print("\n[Step 6] Evaluating Model...")

# Evaluate on test data
test_loss, test_accuracy = model.evaluate(X_test, y_test, verbose=0)
print(f"\nTest Loss: {test_loss:.4f}")
print(f"Test Accuracy: {test_accuracy:.4f} ({test_accuracy*100:.2f}%)")

# Make predictions on test data
y_pred_prob = model.predict(X_test)
y_pred = (y_pred_prob > 0.5).astype(int).flatten()

# Calculate accuracy
accuracy = accuracy_score(y_test, y_pred)
print(f"\nClassification Accuracy: {accuracy:.4f} ({accuracy*100:.2f}%)")

# Confusion Matrix
print("\nConfusion Matrix:")
cm = confusion_matrix(y_test, y_pred)
print(cm)

# Classification Report
print("\nClassification Report:")
class_report = classification_report(y_test, y_pred, target_names=label_encoder.classes_)
print(class_report)

# ============================================================================
# STEP 8: VISUALIZATION
# ============================================================================
print("\n[Step 7] Generating Visualizations...")

# Create figure with subplots
fig, axes = plt.subplots(2, 2, figsize=(14, 10))
fig.suptitle('Rainfall Prediction Model - Performance Analysis', fontsize=16, fontweight='bold')

# Plot 1: Training vs Validation Accuracy
axes[0, 0].plot(history.history['accuracy'], label='Training Accuracy', linewidth=2)
axes[0, 0].plot(history.history['val_accuracy'], label='Validation Accuracy', linewidth=2)
axes[0, 0].set_xlabel('Epoch')
axes[0, 0].set_ylabel('Accuracy')
axes[0, 0].set_title('Training vs Validation Accuracy')
axes[0, 0].legend()
axes[0, 0].grid(True, alpha=0.3)

# Plot 2: Training vs Validation Loss
axes[0, 1].plot(history.history['loss'], label='Training Loss', linewidth=2)
axes[0, 1].plot(history.history['val_loss'], label='Validation Loss', linewidth=2)
axes[0, 1].set_xlabel('Epoch')
axes[0, 1].set_ylabel('Loss')
axes[0, 1].set_title('Training vs Validation Loss')
axes[0, 1].legend()
axes[0, 1].grid(True, alpha=0.3)

# Plot 3: Confusion Matrix Heatmap
sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', ax=axes[1, 0],
            xticklabels=label_encoder.classes_, yticklabels=label_encoder.classes_)
axes[1, 0].set_title('Confusion Matrix')
axes[1, 0].set_ylabel('True Label')
axes[1, 0].set_xlabel('Predicted Label')

# Plot 4: Model Performance Metrics
metrics_names = ['Accuracy', 'Precision (No Rain)', 'Recall (No Rain)', 'Precision (Rain)', 'Recall (Rain)']
metrics_values = [
    accuracy,
    cm[0, 0] / (cm[0, 0] + cm[1, 0]),  # Precision for class 0
    cm[0, 0] / (cm[0, 0] + cm[0, 1]),  # Recall for class 0
    cm[1, 1] / (cm[1, 1] + cm[0, 1]),  # Precision for class 1
    cm[1, 1] / (cm[1, 1] + cm[1, 0])   # Recall for class 1
]

bars = axes[1, 1].bar(metrics_names, metrics_values, color=['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd'])
axes[1, 1].set_ylabel('Score')
axes[1, 1].set_title('Model Performance Metrics')
axes[1, 1].set_ylim([0, 1])
axes[1, 1].grid(True, alpha=0.3, axis='y')

# Add value labels on bars
for i, (bar, value) in enumerate(zip(bars, metrics_values)):
    axes[1, 1].text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.02,
                    f'{value:.3f}', ha='center', va='bottom', fontsize=9)

plt.xticks(rotation=45, ha='right')
plt.tight_layout()
plt.savefig('rainfall_prediction_analysis.png', dpi=300, bbox_inches='tight')
print("Visualization saved as 'rainfall_prediction_analysis.png'")
plt.show()

# ============================================================================
# STEP 9: PREDICTION ON NEW DATA
# ============================================================================
print("\n[Step 8] Making Predictions on Sample Input...")

# Create a sample input for prediction
# Example: Temperature=28.0, Humidity=70, AirPressure=1012.0, WindSpeed=9.0
sample_input = np.array([[28.0, 70, 1012.0, 9.0]])
print(f"\nSample Input (before scaling):")
print(f"Temperature: 28.0°C, Humidity: 70%, AirPressure: 1012.0 hPa, WindSpeed: 9.0 km/h")

# Scale the sample input using the same scaler
sample_input_scaled = scaler.transform(sample_input)
print(f"\nSample Input (after scaling): {sample_input_scaled[0]}")

# Make prediction
prediction_prob = model.predict(sample_input_scaled, verbose=0)
prediction = (prediction_prob > 0.5).astype(int)[0][0]

# Display prediction result
print(f"\nPrediction Probability: {prediction_prob[0][0]:.4f}")

if prediction == 1:
    predicted_class = label_encoder.classes_[1]
    print(f"\n>>> PREDICTION: {predicted_class.upper()} EXPECTED <<<")
else:
    predicted_class = label_encoder.classes_[0]
    print(f"\n>>> PREDICTION: {predicted_class.upper()} <<<")

# ============================================================================
# STEP 10: SAVE THE TRAINED MODEL
# ============================================================================
print("\n[Step 9] Saving Trained Model...")

model_path = 'rainfall_model.h5'
model.save(model_path)
print(f"Model saved successfully as '{model_path}'!")

# Save scaler for future use
import pickle
scaler_path = 'scaler.pkl'
with open(scaler_path, 'wb') as f:
    pickle.dump(scaler, f)
print(f"Scaler saved successfully as '{scaler_path}'!")

# Save label encoder for future use
encoder_path = 'label_encoder.pkl'
with open(encoder_path, 'wb') as f:
    pickle.dump(label_encoder, f)
print(f"Label Encoder saved successfully as '{encoder_path}'!")

# ============================================================================
# PROJECT COMPLETION
# ============================================================================
print("\n" + "="*70)
print("RAINFALL PREDICTION PROJECT COMPLETED SUCCESSFULLY!")
print("="*70)
print("\nGenerated Files:")
print("  1. rainfall_model.h5 - Trained neural network model")
print("  2. scaler.pkl - StandardScaler for feature normalization")
print("  3. label_encoder.pkl - Label encoder for target variable")
print("  4. rainfall_prediction_analysis.png - Performance visualizations")
print("\nModel Performance Summary:")
print(f"  - Test Accuracy: {test_accuracy:.4f} ({test_accuracy*100:.2f}%)")
print(f"  - Epochs: 20")
print(f"  - Batch Size: 32")
print(f"  - Architecture: 64 -> 32 -> 1 (with Dropout)")
print("="*70)
