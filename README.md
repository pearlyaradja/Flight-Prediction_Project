# ✈️ Flight Prediction & Customer Satisfaction Model

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://your-app-url.streamlit.app) [![Python 3.8+](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/downloads/) [![scikit-learn](https://img.shields.io/badge/scikit--learn-1.3.0-orange.svg)](https://scikit-learn.org/)

## 📊 Project Overview

Portfolio project yang menggunakan **Machine Learning** untuk memprediksi:
1. **✈️ Keterlambatan Penerbangan** (Flight Delay Prediction)
2. **😊 Kepuasan Pelanggan** (Customer Satisfaction Prediction)

Proyek ini menggabungkan **Data Analysis**, **Feature Engineering**, **Model Training**, dan **Web Deployment**.

---

## 🎯 Features

### 1. Flight Delay Prediction Model
- Prediksi kemungkinan penerbangan terlambat
- Input: Data maskapai, bandara, jadwal, kondisi cuaca, dll
- Output: Binary classification dengan confidence score
- **Accuracy: ~92% | F1-Score: 0.91**

### 2. Customer Satisfaction Model
- Prediksi tingkat kepuasan penumpang
- Input: Data penumpang, layanan, fasilitas, harga, dll
- Output: Classification dengan confidence score
- **Accuracy: ~88% | F1-Score: 0.87**

### 3. Interactive Web App
- Built dengan Streamlit untuk UX yang user-friendly
- Real-time predictions dengan confidence scores
- Model performance visualization
- Responsive design

---

## 📁 Project Structure

```
flight-prediction-project/
├── 📄 app.py                              # Streamlit web application
├── 📄 requirements.txt                    # Python dependencies
├── 📄 README.md                           # Project documentation
├── 📄 DEPLOYMENT_GUIDE.md                 # Deployment instructions
├── 📄 .gitignore                          # Git configuration
├── 📁 models/                             # Pre-trained models
├── 📁 notebooks/                          # Jupyter notebooks
├── 📁 data/                               # Raw datasets
└── 📁 .streamlit/                         # Streamlit config
```

---

## 🛠️ Technologies Used

| Category | Technology |
|----------|-----------|
| **Language** | Python 3.8+ |
| **Data** | Pandas, NumPy |
| **ML** | Scikit-learn, Random Forest |
| **Web** | Streamlit |
| **Visualization** | Matplotlib, Seaborn, Plotly |
| **Deployment** | Streamlit Cloud / Vercel |

---

## 🚀 Quick Start

### Lokal Development

```bash
# Clone repository
git clone https://github.com/yourusername/flight-prediction-project.git
cd flight-prediction-project

# Create & activate virtual environment
python -m venv venv
venv\Scripts\activate  # Windows
# source venv/bin/activate  # macOS/Linux

# Install dependencies
pip install -r requirements.txt

# Run Streamlit app
streamlit run app.py
```

**App akan buka di:** `http://localhost:8501`

---

## 📈 Model Performance

### Flight Delay Model
| Metric | Score |
|--------|-------|
| Accuracy | 92.34% |
| Precision | 0.918 |
| Recall | 0.923 |
| F1-Score | 0.9206 |

### Customer Satisfaction Model
| Metric | Score |
|--------|-------|
| Accuracy | 88.12% |
| Precision | 0.8745 |
| Recall | 0.8756 |
| F1-Score | 0.8750 |

---

## 🌐 Deployment

### ✅ Streamlit Cloud (RECOMMENDED)
**Fastest & easiest way to share**
1. Push to GitHub
2. Go to https://share.streamlit.io/
3. Connect repository & deploy
4. Get live URL instantly

Lihat [DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md) untuk detail lengkap.

---

## 📚 Notebooks

| Notebook | Focus |
|----------|-------|
| `01_EDA_Flight_Delay.ipynb` | Exploratory data analysis |
| `02_EDA_Customer_Satisfaction.ipynb` | Customer behavior analysis |
| `03_Flight_Delay_Model.ipynb` | Model training & evaluation |
| `04_Customer_Satisfaction_Model.ipynb` | Model training & evaluation |

---

## 💡 Key Skills Demonstrated

✅ Data Analysis & EDA  
✅ Feature Engineering  
✅ Machine Learning & Scikit-learn  
✅ Model Training & Hyperparameter Tuning  
✅ Web Development (Streamlit)  
✅ Cloud Deployment  
✅ Git & GitHub  
✅ Python Programming  

---

## 📞 Support

Buka issue di GitHub atau hubungi untuk pertanyaan.

**Happy Coding! 🚀**
