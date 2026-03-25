# Flight Analytics ML Dashboard - Deployment Guide

## Quick Deploy to Streamlit Cloud

### Prerequisites
- GitHub account
- Streamlit Cloud account (free at https://streamlit.io/cloud)
- Project files pushed to GitHub

### Step 1: Push to GitHub

```bash
# Initialize git (if not already done)
git init

# Add all files
git add .

# Create first commit
git commit -m "Initial commit: Flight Analytics ML Dashboard"

# Add remote repository
git remote add origin https://github.com/YOUR_USERNAME/flight-prediction-project.git

# Push to GitHub
git branch -M main
git push -u origin main
```

### Step 2: Deploy to Streamlit Cloud

1. Go to https://streamlit.io/cloud
2. Click "New app"
3. Select your GitHub repository
4. Set the main file to `app.py`
5. Click "Deploy"

Your app will be live at: `https://[username]-flight-prediction-project.streamlit.app`

---

## Local Development Setup

### Installation

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### Running Locally

```bash
streamlit run app.py
```

The app will be available at `http://localhost:8501`

---

## Project Structure

```
flight-prediction-project/
├── app.py                      # Main Streamlit application
├── requirements.txt            # Python dependencies
├── .streamlit/
│   └── config.toml            # Streamlit configuration
├── models/                     # Pre-trained ML models (.pkl files)
├── data/                       # Dataset files
│   ├── flight_delay/
│   └── passenger_satisfaction/
├── notebooks/                  # Jupyter notebooks for analysis
│   ├── 01_EDA_Flight_Delay.ipynb
│   ├── 02_EDA_Customer_Satisfaction.ipynb
│   ├── 03_Flight_Delay_Model.ipynb
│   └── 04_Customer_Satisfaction_Model.ipynb
└── README.md                   # Project overview
```

---

## Environment Variables (if needed)

Create a `.streamlit/secrets.toml` file for sensitive information:

```toml
# Example API keys (not required for this project)
api_key = "your-api-key-here"
```

---

## Troubleshooting

### Models Not Loading
- Ensure all `.pkl` files are in the `models/` directory
- Check file permissions
- Verify pickle compatibility between Python versions

### Import Errors
- Reinstall dependencies: `pip install -r requirements.txt --force-reinstall`
- Check Python version (3.8+)

### Slow Loading
- Clear Streamlit cache: `streamlit cache clear`
- Optimize model loading with `@st.cache_resource`

---

## Performance Metrics

- **Flight Delay Model**: 92.3% Accuracy
- **Satisfaction Model**: 88.1% Accuracy
- **Prediction Time**: <100ms per request
- **Dataset Size**: 100K+ records each

---

## Contact

- **Email**: mhanifpearlyaradja@gmail.com, nesharizqika@gmail.com
- **GitHub**: https://github.com/pearlyaradja
- **LinkedIn**: http://linkedin.com/in/hanif-pearlyaradja-9637b42a4

---

## License

This project is part of a portfolio demonstration. Feel free to fork and adapt!
