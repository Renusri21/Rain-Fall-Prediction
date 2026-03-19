"""
Rainfall Prediction System - Flask Application Setup Verification
==================================================================
This script verifies that all requirements are met for running the Flask web application.

Usage:
    python verify_flask_setup.py

"""

import os
import sys
import importlib.util
from pathlib import Path

print("\n" + "="*75)
print(" "*15 + "FLASK APPLICATION SETUP VERIFICATION")
print("="*75 + "\n")

# ============================================================================
# Initialize result tracking
# ============================================================================
checks_passed = 0
checks_failed = 0
warnings = 0

def check_passed(message):
    global checks_passed
    checks_passed += 1
    print(f"✓ PASS: {message}")

def check_failed(message):
    global checks_failed
    checks_failed += 1
    print(f"✗ FAIL: {message}")

def check_warning(message):
    global warnings
    warnings += 1
    print(f"⚠ WARN: {message}")

# ============================================================================
# 1. Check Python Version
# ============================================================================
print("\n[1] PYTHON ENVIRONMENT")
print("-" * 75)

python_version = sys.version_info
print(f"Python Version: {python_version.major}.{python_version.minor}.{python_version.micro}")

if python_version.major >= 3 and python_version.minor >= 7:
    check_passed(f"Python 3.{python_version.minor} is supported")
else:
    check_failed(f"Python {python_version.major}.{python_version.minor} is too old (require 3.7+)")

print(f"Python Executable: {sys.executable}")

# ============================================================================
# 2. Check Required Python Packages
# ============================================================================
print("\n[2] REQUIRED PYTHON PACKAGES")
print("-" * 75)

required_packages = {
    'flask': 'Flask',
    'numpy': 'NumPy',
    'pandas': 'Pandas',
    'sklearn': 'Scikit-learn',
}

for package_import, package_name in required_packages.items():
    spec = importlib.util.find_spec(package_import)
    
    if spec is not None:
        try:
            module = importlib.import_module(package_import)
            version = getattr(module, '__version__', 'unknown')
            check_passed(f"{package_name} is installed (version: {version})")
        except Exception as e:
            check_failed(f"{package_name} installation check failed: {str(e)}")
    else:
        check_failed(f"{package_name} is not installed")
        print(f"         Install using: pip install {package_import}")

# ============================================================================
# 3. Check Project Files
# ============================================================================
print("\n[3] PROJECT FILES")
print("-" * 75)

project_root = Path('.')
required_files = {
    'flask_web_app.py': 'Flask application',
    'templates/index.html': 'Web interface template',
    'rainfall_model.pkl': 'Trained ML model',
    'scaler.pkl': 'Feature scaler',
    'label_encoder.pkl': 'Label encoder',
}

for file_path, description in required_files.items():
    full_path = project_root / file_path
    
    if full_path.exists():
        size = full_path.stat().st_size
        check_passed(f"{description} exists ({size} bytes) - {file_path}")
    else:
        check_failed(f"{description} NOT FOUND - {file_path}")

# ============================================================================
# 4. Check Directory Structure
# ============================================================================
print("\n[4] DIRECTORY STRUCTURE")
print("-" * 75)

templates_dir = project_root / 'templates'
if templates_dir.exists() and templates_dir.is_dir():
    check_passed(f"Templates directory exists")
else:
    check_failed(f"Templates directory does not exist")

# ============================================================================
# 5. Test Model Loading
# ============================================================================
print("\n[5] MODEL LOADING TEST")
print("-" * 75)

try:
    import pickle
    
    # Test model
    try:
        with open('rainfall_model.pkl', 'rb') as f:
            model = pickle.load(f)
        check_passed(f"Model loaded successfully (type: {type(model).__name__})")
    except Exception as e:
        check_failed(f"Failed to load model: {str(e)}")
    
    # Test scaler
    try:
        with open('scaler.pkl', 'rb') as f:
            scaler = pickle.load(f)
        check_passed(f"Scaler loaded successfully (type: {type(scaler).__name__})")
    except Exception as e:
        check_failed(f"Failed to load scaler: {str(e)}")
    
    # Test label encoder
    try:
        with open('label_encoder.pkl', 'rb') as f:
            label_encoder = pickle.load(f)
        classes = list(label_encoder.classes_)
        check_passed(f"Label encoder loaded successfully (classes: {classes})")
    except Exception as e:
        check_failed(f"Failed to load label encoder: {str(e)}")
        
except Exception as e:
    check_failed(f"Critical error during model loading: {str(e)}")

# ============================================================================
# 6. Test Flask Application Import
# ============================================================================
print("\n[6] FLASK APPLICATION TEST")
print("-" * 75)

try:
    from flask import Flask, render_template, request, jsonify
    check_passed("Flask imports successful")
    
    # Check if index.html has required form fields
    html_path = project_root / 'templates' / 'index.html'
    if html_path.exists():
        with open(html_path, 'r', encoding='utf-8') as f:
            html_content = f.read()
        
        required_fields = ['temperature', 'humidity', 'pressure', 'wind_speed']
        for field in required_fields:
            if field in html_content:
                check_passed(f"HTML template contains '{field}' field")
            else:
                check_failed(f"HTML template missing '{field}' field")
        
        if '/predict' in html_content:
            check_passed("HTML template references /predict endpoint")
        else:
            check_failed("HTML template does not reference /predict endpoint")
            
except ImportError as e:
    check_failed(f"Flask import failed: {str(e)}")
except Exception as e:
    check_failed(f"Flask application test failed: {str(e)}")

# ============================================================================
# 7. Port Availability Check
# ============================================================================
print("\n[7] PORT AVAILABILITY")
print("-" * 75)

try:
    import socket
    
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    result = sock.connect_ex(('127.0.0.1', 5000))
    sock.close()
    
    if result == 0:
        check_warning("Port 5000 is already in use (may indicate another Flask instance running)")
    else:
        check_passed("Port 5000 is available")
except Exception as e:
    check_warning(f"Could not check port availability: {str(e)}")

# ============================================================================
# Summary Report
# ============================================================================
print("\n" + "="*75)
print(" "*30 + "VERIFICATION SUMMARY")
print("="*75)

total_checks = checks_passed + checks_failed
success_rate = (checks_passed / total_checks * 100) if total_checks > 0 else 0

print(f"\nTotal Checks: {total_checks}")
print(f"  ✓ Passed: {checks_passed}")
print(f"  ✗ Failed: {checks_failed}")
if warnings > 0:
    print(f"  ⚠ Warnings: {warnings}")

print(f"  Success Rate: {success_rate:.1f}%")

# ============================================================================
# Status and Recommendations
# ============================================================================
print("\n" + "="*75)
print(" "*35 + "STATUS")
print("="*75)

if checks_failed == 0:
    print("\n✓✓✓ ALL CHECKS PASSED ✓✓✓")
    print("\nYour Flask application is ready to run!")
    print("\nTo start the application, run:")
    print("  python flask_web_app.py")
    print("\nThen open your browser to:")
    print("  http://localhost:5000/")
    sys.exit(0)
else:
    print(f"\n✗✗✗ {checks_failed} CHECK(S) FAILED ✗✗✗")
    print("\nPlease fix the above issues before running the Flask application.")
    
    if checks_failed > 0:
        print("\nQuick fixes:")
        print("  1. Missing packages: pip install flask numpy pandas scikit-learn")
        print("  2. Missing model files: python rainfall_prediction_sklearn.py")
        print("  3. Missing templates: Ensure templates/ folder exists")
    
    sys.exit(1)
