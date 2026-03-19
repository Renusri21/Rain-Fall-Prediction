# ============================================================================
# RAINFALL PREDICTION USING NEURAL NETWORKS (Scikit-learn)
# ============================================================================
# This script predicts rainfall (Yes/No) based on meteorological features
# using a Multi-layer Perceptron (MLP) Neural Network from scikit-learn
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
from sklearn.neural_network import MLPClassifier
import warnings
import time

# Suppress warnings for cleaner output
warnings.filterwarnings('ignore')

# Set random seeds for reproducibility
np.random.seed(42)

print("="*70)
print("RAINFALL PREDICTION USING NEURAL NETWORKS (Scikit-learn)")
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
print("\n[Step 3] Building Neural Network Model (MLP)...")

# Get number of input features
num_features = X_train.shape[1]

# Create MLP model (Multi-layer Perceptron)
# Architecture: Input -> 64 -> 32 -> 1 (Output)
model = MLPClassifier(
    hidden_layer_sizes=(64, 32),           # Two hidden layers with 64 and 32 neurons
    activation='relu',                      # ReLU activation function
    solver='adam',                          # Adam optimizer
    alpha=0.0001,                           # L2 regularization
    batch_size=32,                          # Batch size
    learning_rate='adaptive',               # Adaptive learning rate
    learning_rate_init=0.001,               # Initial learning rate
    max_iter=100,                           # Number of iterations (epochs)
    early_stopping=True,                    # Stop early if validation score doesn't improve
    validation_fraction=0.2,                # Use 20% for validation
    tol=1e-4,                               # Tolerance
    n_iter_no_change=20,                    # Stop if no improvement for 20 iterations
    random_state=42,
    verbose=1
)

print("Model Architecture:")
print(f"  Input Layer: {num_features} features")
print(f"  Hidden Layer 1: 64 neurons (ReLU activation)")
print(f"  Hidden Layer 2: 32 neurons (ReLU activation)")
print(f"  Output Layer: 1 neuron (2 classes)")
print(f"  Solver: Adam optimizer")
print(f"  Regularization: L2 (Alpha=0.0001)")

# ============================================================================
# STEP 5-6: MODEL TRAINING
# ============================================================================
print("\n[Step 4] Training Model...")
print("Training with up to 100 epochs...\n")

start_time = time.time()
model.fit(X_train, y_train)
training_time = time.time() - start_time

print(f"\nModel training completed in {training_time:.2f} seconds!")
print(f"Converged: {model.n_iter_} iterations")

# Store training history for visualization
train_scores = model.loss_curve_ if hasattr(model, 'loss_curve_') else []
print(f"Final training loss: {model.loss_:.4f}" if hasattr(model, 'loss_') else "")

# ============================================================================
# STEP 7: MODEL EVALUATION
# ============================================================================
print("\n[Step 5] Evaluating Model...")

# Evaluate on training data
train_accuracy = model.score(X_train, y_train)
print(f"\nTraining Accuracy: {train_accuracy:.4f} ({train_accuracy*100:.2f}%)")

# Evaluate on test data
test_accuracy = model.score(X_test, y_test)
print(f"Test Accuracy: {test_accuracy:.4f} ({test_accuracy*100:.2f}%)")

# Make predictions on test data
y_pred = model.predict(X_test)

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
print("\n[Step 6] Generating Visualizations...")

# Create figure with subplots
fig, axes = plt.subplots(2, 2, figsize=(14, 10))
fig.suptitle('Rainfall Prediction Model - Performance Analysis', fontsize=16, fontweight='bold')

# Plot 1: Training Loss Curve
if train_scores:
    axes[0, 0].plot(train_scores, label='Training Loss', linewidth=2, color='#1f77b4')
    axes[0, 0].set_xlabel('Iteration')
    axes[0, 0].set_ylabel('Loss')
    axes[0, 0].set_title('Training Loss Over Iterations')
    axes[0, 0].legend()
    axes[0, 0].grid(True, alpha=0.3)
else:
    axes[0, 0].text(0.5, 0.5, 'Training Loss\n(n/a for this solver)', 
                    ha='center', va='center', fontsize=12)
    axes[0, 0].set_title('Training Loss')
    axes[0, 0].axis('off')

# Plot 2: Model Accuracy Comparison
accuracies = [train_accuracy, test_accuracy]
accuracy_labels = ['Training', 'Test']
colors = ['#2ca02c', '#ff7f0e']
bars = axes[0, 1].bar(accuracy_labels, accuracies, color=colors, alpha=0.7, edgecolor='black', linewidth=2)
axes[0, 1].set_ylabel('Accuracy')
axes[0, 1].set_title('Model Accuracy Comparison')
axes[0, 1].set_ylim([0, 1])
axes[0, 1].grid(True, alpha=0.3, axis='y')

# Add value labels on bars
for bar, acc in zip(bars, accuracies):
    height = bar.get_height()
    axes[0, 1].text(bar.get_x() + bar.get_width()/2., height + 0.02,
                    f'{acc:.3f}', ha='center', va='bottom', fontsize=11, fontweight='bold')

# Plot 3: Confusion Matrix Heatmap
sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', ax=axes[1, 0],
            xticklabels=label_encoder.classes_, yticklabels=label_encoder.classes_,
            cbar_kws={'label': 'Count'})
axes[1, 0].set_title('Confusion Matrix')
axes[1, 0].set_ylabel('True Label')
axes[1, 0].set_xlabel('Predicted Label')

# Plot 4: Model Performance Metrics
# Calculate precision, recall for each class
from sklearn.metrics import precision_recall_fscore_support
precision, recall, f1, _ = precision_recall_fscore_support(y_test, y_pred, average=None)

metrics_names = ['Accuracy', 'Precision\n(No Rain)', 'Recall\n(No Rain)', 
                 'Precision\n(Rain)', 'Recall\n(Rain)']
metrics_values = [
    test_accuracy,
    precision[0] if len(precision) > 0 else 0,
    recall[0] if len(recall) > 0 else 0,
    precision[1] if len(precision) > 1 else 0,
    recall[1] if len(recall) > 1 else 0
]

bars = axes[1, 1].bar(metrics_names, metrics_values, 
                      color=['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd'],
                      alpha=0.7, edgecolor='black', linewidth=1.5)
axes[1, 1].set_ylabel('Score')
axes[1, 1].set_title('Model Performance Metrics')
axes[1, 1].set_ylim([0, 1.1])
axes[1, 1].grid(True, alpha=0.3, axis='y')

# Add value labels on bars
for bar, value in zip(bars, metrics_values):
    height = bar.get_height()
    axes[1, 1].text(bar.get_x() + bar.get_width()/2., height + 0.02,
                    f'{value:.3f}', ha='center', va='bottom', fontsize=9)

plt.xticks(rotation=45, ha='right')
plt.tight_layout()
plt.savefig('rainfall_prediction_analysis.png', dpi=300, bbox_inches='tight')
print("Visualization saved as 'rainfall_prediction_analysis.png'")
# plt.show()  # Commented out to avoid blocking in terminal mode

# ============================================================================
# STEP 9: PREDICTION ON NEW DATA
# ============================================================================
print("\n[Step 7] Making Predictions on Sample Input...")

# Create a sample input for prediction
# Example: Temperature=28.0, Humidity=70, AirPressure=1012.0, WindSpeed=9.0
sample_input = np.array([[28.0, 70, 1012.0, 9.0]])
print(f"\nSample Input (before scaling):")
print(f"Temperature: 28.0°C, Humidity: 70%, AirPressure: 1012.0 hPa, WindSpeed: 9.0 km/h")

# Scale the sample input using the same scaler
sample_input_scaled = scaler.transform(sample_input)
print(f"Sample Input (after scaling): {sample_input_scaled[0]}")

# Make prediction
prediction = model.predict(sample_input_scaled)[0]
prediction_prob = model.predict_proba(sample_input_scaled)[0]

# Display prediction result
print(f"\nPrediction Probabilities:")
for i, prob in enumerate(prediction_prob):
    print(f"  Class '{label_encoder.classes_[i]}': {prob:.4f}")

predicted_class = label_encoder.classes_[prediction]
print(f"\n>>> PREDICTION: {predicted_class.upper()} <<<")

# ============================================================================
# STEP 10: SAVE THE TRAINED MODEL
# ============================================================================
print("\n[Step 8] Saving Trained Model...")

# Save model for future use
import pickle

model_path = 'rainfall_model.pkl'
with open(model_path, 'wb') as f:
    pickle.dump(model, f)
print(f"Model saved successfully as '{model_path}'!")

# Save scaler for future use
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
print("  1. rainfall_model.pkl - Trained neural network model")
print("  2. scaler.pkl - StandardScaler for feature normalization")
print("  3. label_encoder.pkl - Label encoder for target variable")
print("  4. rainfall_prediction_analysis.png - Performance visualizations")
print("\nModel Performance Summary:")
print(f"  - Test Accuracy: {test_accuracy:.4f} ({test_accuracy*100:.2f}%)")
print(f"  - Training Accuracy: {train_accuracy:.4f} ({train_accuracy*100:.2f}%)")
print(f"  - Architecture: Input(4) -> Dense(64) -> Dense(32) -> Output(2)")
print(f"  - Training Time: {training_time:.2f} seconds")
print(f"  - Convergence Iterations: {model.n_iter_}")
print("="*70)
