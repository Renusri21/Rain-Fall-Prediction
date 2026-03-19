# Deploy Flask Rainfall Prediction System to Render

## Quick Deployment Steps

### Step 1: Prepare Your GitHub Repository

```bash
cd C:\RainfallPredictionProject
git add .
git commit -m "Prepare for Render deployment"
git push origin main
```

**Files automatically included:**
- `flask_web_app.py` - Main Flask application ✓
- `requirements.txt` - Python dependencies ✓
- `Procfile` - Deployment configuration ✓
- `templates/` - HTML templates ✓
- `static/` - CSS/JS files (if any) ✓
- `rainfall_model.pkl` - ML model ✓
- `scaler.pkl` - Feature scaler ✓
- `label_encoder.pkl` - Label encoder ✓
- `rainfall_data.csv` - Dataset ✓

---

## Step 2: Deploy on Render

### Method A: Connect GitHub (Recommended)

1. Go to **https://render.com** and sign up (free account)
2. Click **"New +"** → **"Web Service"**
3. Click **"Connect a repository"**
   - Choose: **renusri21/Rain-Fall-Prediction**
4. Fill in these details:
   - **Name**: `rainfall-prediction` (or your preferred name)
   - **Environment**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `python flask_web_app.py`
5. Click **"Create Web Service"**
6. Wait 2-5 minutes for deployment
7. Your URL will be: `https://rainfall-prediction.onrender.com`

### Method B: Manual Deployment

If GitHub connection has issues:

1. Clone locally if needed: `git clone https://github.com/renusri21/Rain-Fall-Prediction.git`
2. Go to Render → **"New Web Service"**
3. Upload files manually or use Render's Git integration

---

## Step 3: Update Your GitHub Pages

Once deployed, update your `README.md` or create an `index.html` in `docs/` folder:

```html
<!DOCTYPE html>
<html>
<head>
    <title>Rainfall Predictor - Deployed</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        }
        .container {
            text-align: center;
            background: white;
            padding: 40px;
            border-radius: 10px;
            box-shadow: 0 10px 25px rgba(0,0,0,0.2);
        }
        a {
            display: inline-block;
            margin-top: 20px;
            padding: 12px 30px;
            background: #667eea;
            color: white;
            text-decoration: none;
            border-radius: 5px;
            font-weight: bold;
        }
        a:hover {
            background: #764ba2;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>🌧️ Rainfall Prediction System</h1>
        <p>Live deployment ready!</p>
        <a href="https://rainfall-prediction.onrender.com" target="_blank">
            🚀 Open Application
        </a>
    </div>
</body>
</html>
```

Then push this to your repository:
```bash
git add docs/index.html
git commit -m "Add deployment redirect"
git push origin main
```

---

## Step 4: Access Your Application

### Local (Development)
```bash
python flask_web_app.py
# Open: http://localhost:5000
```

### Cloud (Production)
```
https://rainfall-prediction.onrender.com
```

---

## Troubleshooting

### Issue: Build fails

**Solution**: Check the build logs in Render dashboard
- Click your service → "Logs" tab
- Common issues:
  - Missing `requirements.txt` → Add it
  - Wrong Python version → Use Python 3.9+
  - Missing files → Ensure all `.pkl` files are committed

### Issue: Application crashes after deployment

**Solution**: 
1. Restart the service (Render dashboard → "Manual Deploy")
2. Check logs for errors
3. Ensure `flask_web_app.py` uses `PORT` environment variable (already done ✓)

### Issue: Model files not found

**Solution**: 
- Ensure `.pkl` files are in the root directory
- If using Git LFS, configure it:
  ```bash
  git lfs install
  git lfs track "*.pkl"
  git add .gitattributes
  git commit -m "Track large files with Git LFS"
  ```

---

## Performance Notes

- **Cold Start**: First request may take 30-60 seconds (Render's free tier)
- **Response Time**: Predictions typically respond in 0.1-0.5 seconds
- **Concurrent Users**: Free tier handles ~1000 requests/month

---

## Next: Update GitHub Pages with Link

Update your GitHub Pages site to link to the live application:

**File**: `docs/index.md` or GitHub Pages settings
```markdown
# Rainfall Prediction System

[🚀 **Click here to use the live application**](https://rainfall-prediction.onrender.com)

This system uses machine learning to predict rainfall based on:
- Temperature
- Humidity  
- Air Pressure
- Wind Speed
```

---

## Summary

✅ **Local**: Working on `http://localhost:5000`
✅ **Cloud**: Deployed on `https://rainfall-prediction.onrender.com`
✅ **Accessible**: From anywhere via public URL

Your Flask application is now production-ready and publicly accessible!
