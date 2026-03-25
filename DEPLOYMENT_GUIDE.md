# 🚀 Panduan Deployment

## Opsi 1: Deploy ke Streamlit Cloud (⭐ RECOMMENDED)

Streamlit Cloud adalah pilihan terbaik untuk project ML karena:
- ✅ Gratis untuk public repository
- ✅ Mudah setup
- ✅ Support Python natively
- ✅ Auto-redeploy saat push ke GitHub

### Langkah-langkah:

#### 1. Siapkan Repository GitHub
```bash
# Inisialisasi git (jika belum)
git init
git add .
git commit -m "Initial commit - Flight Prediction App"
git remote add origin https://github.com/USERNAME/flight-prediction-project.git
git push -u origin main
```

#### 2. Deploy ke Streamlit Cloud
1. Buka https://share.streamlit.io/
2. Login dengan GitHub account
3. Click "New app"
4. Pilih repository: `flight-prediction-project`
5. Branch: `main`
6. File path: `app.py`
7. Click "Deploy"

**Selesai! Aplikasi akan live dalam beberapa menit.**

---

## Opsi 2: Deploy ke Vercel (dengan Flask API)

Vercel lebih cocok untuk web app tradisional. Untuk project ini:

### Setup Flask API

1. **Install Flask:**
```bash
pip install flask flask-cors
```

2. **Buat `api/predict.py`:**
```python
from flask import Flask, request, jsonify
import pickle
import numpy as np
import pandas as pd
from pathlib import Path

app = Flask(__name__)

# Load models
models_dir = Path(__file__).parent.parent / 'models'

@app.route('/api/predict-flight', methods=['POST'])
def predict_flight():
    try:
        data = request.json
        model = pickle.load(open(models_dir / 'flight_delay_model.pkl', 'rb'))
        # Process and predict
        prediction = model.predict([[...]])
        return jsonify({'prediction': prediction[0].tolist()})
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/api/predict-satisfaction', methods=['POST'])
def predict_satisfaction():
    try:
        data = request.json
        model = pickle.load(open(models_dir / 'satisfaction_model.pkl', 'rb'))
        # Process and predict
        prediction = model.predict([[...]])
        return jsonify({'prediction': prediction[0].tolist()})
    except Exception as e:
        return jsonify({'error': str(e)}), 400

if __name__ == '__main__':
    app.run(debug=True)
```

3. **Setup Vercel:**
```bash
npm install -g vercel
vercel login
vercel
```

---

## Opsi 3: Deploy Lokal (untuk Testing)

### Jalankan di lokal:
```bash
# Install dependencies
pip install -r requirements.txt

# Run Streamlit app
streamlit run app.py

# Aplikasi akan buka di http://localhost:8501
```

---

## 📁 File Structure untuk Deployment

```
flight-prediction-project/
├── app.py                    # Main Streamlit app
├── requirements.txt          # Python dependencies
├── README.md                 # Project documentation
├── DEPLOYMENT_GUIDE.md       # File ini
├── .gitignore               # Git ignore rules
├── .streamlit/
│   └── config.toml          # Streamlit configuration
├── models/
│   ├── flight_delay_model.pkl
│   ├── flight_delay_scaler.pkl
│   ├── flight_delay_features.pkl
│   ├── flight_delay_label_encoders.pkl
│   ├── satisfaction_model.pkl
│   ├── satisfaction_scaler.pkl
│   ├── satisfaction_features.pkl
│   └── satisfaction_label_encoders.pkl
├── notebooks/
│   ├── 01_EDA_Flight_Delay.ipynb
│   ├── 02_EDA_Customer_Satisfaction.ipynb
│   ├── 03_Flight_Delay_Model.ipynb
│   └── 04_Customer_Satisfaction_Model.ipynb
└── data/
    ├── flight_delay/
    └── passenger_satisfaction/
```

---

## 🔑 Environment Variables (jika diperlukan)

Buat `.env` file untuk local development:
```
STREAMLIT_SERVER_HEADLESS=true
STREAMLIT_SERVER_PORT=8501
```

---

## ✅ Checklist Sebelum Deploy

- [ ] Git repository sudah di-push ke GitHub
- [ ] Semua model files ada di folder `/models/`
- [ ] `requirements.txt` sudah updated
- [ ] `app.py` bisa dijalankan di lokal tanpa error
- [ ] `.gitignore` sudah setup dengan benar
- [ ] README.md sudah lengkap describe project

---

## 🎯 Rekomendasi

**Gunakan Streamlit Cloud** karena:
1. **Paling Simple** - Tinggal connect GitHub, langsung deploy
2. **Cocok untuk ML** - Built-in support untuk Python ML libs
3. **Gratis** - Unlimited public deployments
4. **Auto-update** - Setiap push ke GitHub otomatis update app

**URL deployment akan seperti:**
```
https://projectname-username.streamlit.app
```

---

## 📝 Tips Portfolio

Untuk membuat portfolio lebih menarik:

1. **Tambahkan GitHub Badge:**
   ```markdown
   [![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://your-app-url.streamlit.app)
   ```

2. **Lengkapi README dengan:**
   - Project description
   - Features
   - Model performance metrics
   - How to use
   - Technologies used

3. **Showcase di Portfolio/LinkedIn:**
   - Link ke live app
   - GitHub repository link
   - Demo screenshot/video

---

## 🆘 Troubleshooting

**Error: Model file not found**
```
Solution: Git add/commit dan push ulang model files
```

**Error: Package not installed**
```
Solution: Update requirements.txt dan push ulang
```

**App loading slowly**
```
Solution: Cache models dengan @st.cache_resource
```

---

**Happy Deploying! 🚀**
