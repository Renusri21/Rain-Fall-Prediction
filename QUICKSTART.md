# QUICK START GUIDE - Rainfall Prediction Project

## Project Location
**Windows:** `C:\RainfallPredictionProject\`

## What's Included

✅ **rainfall_prediction.py** - Complete main script with all requirements
✅ **rainfall_data.csv** - Sample meteorological dataset (50 records)
✅ **requirements.txt** - All required dependencies
✅ **run_project.bat** - One-click Windows batch script
✅ **README.md** - Comprehensive documentation
✅ **QUICKSTART.md** - This file

## Quick Start (3 Steps)

### Option 1: Automatic Setup (Recommended for Windows)
1. Double-click `run_project.bat`
2. Wait for installation and execution
3. View results and generated files

### Option 2: Manual Setup
1. Open PowerShell/Command Prompt
2. Navigate to `C:\RainfallPredictionProject`
   ```bash
   cd C:\RainfallPredictionProject
   ```

3. Install dependencies
   ```bash
   pip install -r requirements.txt
   ```

4. Run the project
   ```bash
   python rainfall_prediction.py
   ```

### Option 3: VS Code (Recommended)
1. Open VS Code
2. Open the folder: `C:\RainfallPredictionProject`
3. Install required extensions:
   - Python (Microsoft)
   - Pylance
4. Open terminal and install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
5. Right-click `rainfall_prediction.py` and select "Run Python File in Terminal"
   OR press `Ctrl+F5`

## What the Script Does

| Step | Description |
|------|-------------|
| 1 | Loads meteorological data from CSV |
| 2 | Preprocesses and scales features |
| 3 | Builds neural network model (64→32→1) |
| 4 | Trains model for 20 epochs |
| 5 | Evaluates accuracy on test data |
| 6 | Generates performance visualizations |
| 7 | Makes predictions on sample data |
| 8 | Saves trained model as H5 file |

## Expected Output Files

After running, you'll have:
- ✅ `rainfall_model.h5` - Trained model (binary format)
- ✅ `scaler.pkl` - Feature normalizer
- ✅ `label_encoder.pkl` - Target encoder
- ✅ `rainfall_prediction_analysis.png` - Performance charts

## Typical Output

```
Dataset Shape: (50, 5)
First 5 rows: [display of data]
...
Test Accuracy: 0.9000 (90.00%)

Confusion Matrix:
[[8 1]
 [1 9]]

Training completed!
Model saved as 'rainfall_model.h5'
```

## System Requirements

- **OS:** Windows 10/11 (or macOS/Linux with Python 3.7+)
- **Python:** 3.7 or higher
- **RAM:** 2GB minimum (4GB+ recommended)
- **Disk:** ~500MB (for dependencies)

## Features Included

✅ Complete error handling
✅ Data validation and statistics
✅ Feature normalization with StandardScaler
✅ Proper train-test split (80-20)
✅ Dropout regularization (30%)
✅ Binary classification with Sigmoid activation
✅ Comprehensive evaluation metrics
✅ Confusion matrix and classification report
✅ 4 visualization plots
✅ Model persistence (H5 format)
✅ Pickle serialization of utilities
✅ Thoroughly commented code
✅ Multiple prediction examples

## Model Architecture

```
Input (4 features)
    ↓
Dense 64 (ReLU) + Dropout(0.3)
    ↓
Dense 32 (ReLU) + Dropout(0.3)
    ↓
Output 1 (Sigmoid)
    ↓
Binary Classification (Yes/No)
```

## Training Details

- **Optimizer:** Adam
- **Loss:** Binary Crossentropy
- **Metrics:** Accuracy
- **Epochs:** 20
- **Batch Size:** 32
- **Validation Split:** 20%

## Troubleshooting

### Problem: "Python command not found"
- Solution: Install Python from https://www.python.org/
- Add Python to PATH during installation

### Problem: "No module named 'tensorflow'"
- Solution: `pip install tensorflow`
- It may take several minutes to install

### Problem: "File not found: rainfall_data.csv"
- Solution: Ensure CSV is in same directory as Python script

### Problem: Script runs slow
- Solution: This is normal on first run (TensorFlow initialization)
- Subsequent runs will be faster

## Advanced Usage

### Load and use the saved model:
```python
import pickle
from tensorflow.keras.models import load_model

model = load_model('rainfall_model.h5')
with open('scaler.pkl', 'rb') as f:
    scaler = pickle.load(f)

# Make prediction
new_data = scaler.transform([[28, 70, 1012, 9]])
prediction = model.predict(new_data)
```

### Modify dataset:
- Edit `rainfall_data.csv` with your own data
- Keep same column names and format

### Adjust model hyperparameters:
- Open `rainfall_prediction.py`
- Modify Dense layers, Dropout values, epochs, batch_size
- Re-run the script

## Key Code Sections

| Section | Line Range | Purpose |
|---------|-----------|---------|
| Imports | 1-25 | Library imports |
| Load Data | 40-60 | CSV loading and exploration |
| Preprocessing | 65-110 | Data cleaning and scaling |
| Model Building | 115-130 | Neural network architecture |
| Training | 140-160 | Model training |
| Evaluation | 165-190 | Performance metrics |
| Visualization | 195-250 | Plot generation |
| Prediction | 255-280 | Sample predictions |
| Save Model | 285-300 | Model serialization |

## Success Indicators

✅ Script runs without errors
✅ Test accuracy displayed (typically 80-95%)
✅ 4 plots generated in visualization
✅ Model saved as rainfall_model.h5
✅ "COMPLETED SUCCESSFULLY" message shown

## Next Steps

1. ✅ Run the project successfully
2. ✅ Review the generated visualizations
3. ✅ Modify the CSV with different data
4. ✅ Adjust hyperparameters for better accuracy
5. ✅ Deploy the model to make predictions

## Need Help?

- Read `README.md` for detailed documentation
- Check script comments for explanations
- Verify Python and package versions
- Ensure sufficient disk space for TensorFlow

## File Descriptions

| File | Size | Purpose |
|------|------|---------|
| rainfall_prediction.py | ~15KB | Main script |
| rainfall_data.csv | ~2KB | Training data |
| requirements.txt | <1KB | Dependencies |
| run_project.bat | ~2KB | Windows launcher |
| README.md | ~10KB | Full documentation |
| QUICKSTART.md | ~5KB | This file |

---

**Project Created:** March 2026
**Framework:** TensorFlow/Keras
**Task:** Binary Classification (Rainfall Prediction)
**Status:** Ready to Run ✅
