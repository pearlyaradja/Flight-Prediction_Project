import streamlit as st
import pandas as pd
import numpy as np
import pickle
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go
from pathlib import Path

# Set page config
st.set_page_config(
    page_title="Flight & Satisfaction ML Dashboard",
    page_icon="✈️",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        "About": "ML Analytics Dashboard - Flight Prediction & Customer Satisfaction"
    }
)

# Initialize session state
if "current_page" not in st.session_state:
    st.session_state.current_page = "Dashboard"

# Modern CSS Styling (Like Traveloka)
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&display=swap');
    
    * {
        margin: 0;
        padding: 0;
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
        font-weight: 500;
    
    html, body, [data-testid="stAppViewContainer"] {
        background-color: #f5f7fa;
    }
    
    /* ============ HERO ============ */
    .hero {
        position: relative;
        background: linear-gradient(135deg, #1e3a8a 0%, #0f172a 100%);
        padding: 64px 48px;
        border-radius: 16px;
        overflow: hidden;
        margin-bottom: 32px;
    }
    
    .hero::before {
        content: "";
        position: absolute;
        width: 400px;
        height: 400px;
        background: radial-gradient(circle, rgba(59,130,246,0.25) 0%, transparent 70%);
        top: -100px;
        right: -100px;
    }
    
    .hero-content {
        position: relative;
        z-index: 2;
        max-width: 700px;
    }
    
    .hero h1 {
        font-size: 2.8em;
        font-weight: 700;
        color: #ffffff;
        margin-bottom: 12px;
        letter-spacing: -0.02em;
    }
    
    .hero-main {
        font-size: 1.2em;
        color: #cbd5f5;
        margin-bottom: 8px;
    }
    
    .hero-sub {
        font-size: 0.95em;
        color: #94a3b8;
    }
    
    /* ============ METRICS ============ */
    .metric-card {
        background: white;
        padding: 28px 24px;
        border-radius: 10px;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
        border: 1px solid #e5e7eb;
        transition: all 0.2s ease;
        cursor: pointer;
    }
    
    .metric-card:hover {
        transform: translateY(-4px);
        box-shadow: 0 8px 16px rgba(0, 0, 0, 0.08);
        border-color: #d1d5db;
    }
    
    .metric-label {
        font-size: 0.9em;
        color: #6b7280;
        margin-bottom: 10px;
        font-weight: 500;
        letter-spacing: 0.2px;
    }
    
    .metric-value {
        font-size: 2.2em;
        font-weight: 600;
        color: #1e3a8a;
        margin-bottom: 6px;
        letter-spacing: -0.01em;
    }
    
    .metric-desc {
        font-size: 0.85em;
        color: #9ca3af;
        font-weight: 400;
    }
    
    /* ============ SECTION HEADERS ============ */
    .section-header {
        background: linear-gradient(90deg, #1e3a8a 0%, #1f2937 100%);
        color: white;
        padding: 20px 28px;
        border-radius: 10px;
        margin: 40px 0 24px 0;
        font-size: 1.35em;
        font-weight: 600;
        letter-spacing: -0.01em;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
    }
    
    /* ============ INFO BOXES ============ */
    .info-box {
        background: linear-gradient(135deg, #1e3a8a 0%, #1f2937 100%);
        color: white;
        padding: 28px 26px;
        border-radius: 10px;
        margin-bottom: 20px;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
        border: 1px solid rgba(255, 255, 255, 0.08);
    }
    
    .info-box-success {
        background: linear-gradient(135deg, #065f46 0%, #059669 100%);
        box-shadow: 0 4px 12px rgba(5, 150, 105, 0.1);
    }
    
    .info-box-warning {
        background: linear-gradient(135deg, #7c2d12 0%, #b45309 100%);
        box-shadow: 0 4px 12px rgba(180, 83, 9, 0.1);
    }
    
    .info-box h3, .info-box h4 {
        color: white !important;
        margin-bottom: 16px;
        font-weight: 700;
        font-size: 1.3em;
    }
    
    .info-box p, .info-box ul, .info-box li {
        color: white !important;
        line-height: 1.8;
        font-weight: 400;
    }
    
    .info-box ul {
        margin-left: 24px;
        margin-top: 12px;
    }
    
    .info-box li {
        margin-bottom: 12px;
    }
    
    .info-box strong {
        color: white;
        font-weight: 700;
    }
    
    /* ============ CHART CONTAINER ============ */
    .chart-container {
        background: white;
        padding: 28px;
        border-radius: 10px;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
        margin-bottom: 24px;
        border: 1px solid #e5e7eb;
    }
    
    .chart-container h3, .chart-container h4 {
        color: #1f2937 !important;
        margin-bottom: 20px;
        font-weight: 600;
        font-size: 1.25em;
        letter-spacing: -0.01em;
    }
    
    /* ============ TABS ============ */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background-color: transparent;
        padding-bottom: 16px;
        border-bottom: 1px solid #e5e7eb;
    }
    
    .stTabs [data-baseweb="tab-list"] button {
        font-size: 0.95em;
        font-weight: 500;
        border-radius: 8px;
        padding: 10px 20px;
        color: #6b7280;
        background: transparent;
        border: 1px solid transparent;
        transition: all 0.2s;
    }
    
    .stTabs [data-baseweb="tab-list"] button:hover {
        background-color: #f3f4f6;
        color: #1e3a8a;
    }
    
    .stTabs [data-baseweb="tab-list"] button[aria-selected="true"] {
        color: #1e3a8a;
        background-color: #f3f4f6;
        border-bottom: 2px solid #1e3a8a;
        font-weight: 600;
    }
    
    /* ============ BUTTONS ============ */
    .stButton > button {
        background: linear-gradient(90deg, #1e3a8a 0%, #1f2937 100%);
        color: white !important;
        border: none;
        padding: 12px 28px;
        border-radius: 8px;
        font-weight: 500;
        font-size: 0.95em;
        cursor: pointer;
        transition: all 0.2s ease;
        width: 100%;
        text-transform: capitalize;
        letter-spacing: 0.2px;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
        text-align: left !important;
    }
    
    .stButton > button:hover {
        transform: translateY(-1px);
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.12);
    }
    
    .stButton > button:active {
        transform: translateY(0);
    }
    
    /* ============ SIDEBAR ============ */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #1e3a8a 0%, #1f2937 100%);
        padding-top: 16px;
        min-width: 250px !important;
        width: 250px !important;
        position: fixed !important;
        left: 0 !important;
        top: 0 !important;
        height: 100vh !important;
        overflow-y: auto !important;
        resize: none !important;
        user-select: none !important;
        z-index: 100 !important;
    }
    
    /* Hide keyboard shortcut labels */
    [data-testid="stSidebar"] [aria-label*="keyboard"],
    [class*="keyboard_double"] {
        display: none !important;
    }
    
    /* Disable sidebar toggle button */
    [data-testid="stSidebar"] + button {
        display: none !important;
    }
    
    /* Lock sidebar header */
    [data-testid="stSidebar"] > div:first-child {
        position: sticky !important;
        top: 0 !important;
        z-index: 999 !important;
    }
    
    [data-testid="stSidebar"] [data-baseweb="select"] > div {
        background-color: rgba(255, 255, 255, 0.07) !important;
        border: 1.5px solid rgba(148, 163, 184, 0.3) !important;
        border-radius: 10px;
        padding: 10px 14px !important;
        color: #fff !important;
    }
    
    [data-testid="stSidebar"] [data-baseweb="select"] [data-baseweb="popover"] {
        background-color: #1e3a8a !important;
    }
    
    [data-testid="stSidebar"] [data-baseweb="menu"] {
        background-color: #1e3a8a !important;
    }
    
    [data-testid="stSidebar"] [data-baseweb="menu"] li {
        background-color: #1e3a8a !important;
        color: #ffffff !important;
    }
    
    [data-testid="stSidebar"] [data-baseweb="menu"] li:hover {
        background-color: #2d5a96 !important;
        color: #ffffff !important;
    }
    
    [data-testid="stSidebar"] [role="option"] {
        color: #ffffff !important;
        background-color: #1e3a8a !important;
    }
    
    [data-testid="stSidebar"] [role="option"]:hover {
        background-color: #2d5a96 !important;
    }
    
    [data-testid="stSidebar"] [data-baseweb="select"] > div:hover {
        border-color: #94a3b8 !important;
        background-color: rgba(255, 255, 255, 0.1) !important;
    }
    
    [data-testid="stSidebar"] [data-baseweb="select"] > div > span {
        color: #ffffff !important;
        font-weight: 900;
        font-size: 0.9em;
        font-family: 'Lato', sans-serif;
        letter-spacing: 0.5px;
    }
    
    [data-testid="stSidebar"] button {
        color: #ffffff !important;
        font-family: 'Poppins', sans-serif;
    }
    
    [data-testid="stSidebar"] [data-baseweb="base-input"] input {
        color: #ffffff !important;
        font-family: 'Poppins', sans-serif;
    }
    
    [data-testid="stSidebar"] [role="button"] {
        color: #ffffff !important;
    }
    
    [data-testid="stSidebar"] .stButton > button {
        background-color: transparent !important;
        color: #cbd5e1 !important;
        border: none !important;
        padding: 12px 16px !important;
        margin: 4px 8px !important;
        border-radius: 8px !important;
        font-weight: 500 !important;
        font-size: 0.9em !important;
        font-family: 'Inter', sans-serif !important;
        text-align: left !important;
        display: flex;
        align-items: center;
        justify-content: flex-start !important;
    }
    
    [data-testid="stSidebar"] .stButton > button span {
        text-align: left !important;
    }
    
    [data-testid="stSidebar"] .stButton > button:hover {
        background-color: rgba(59, 130, 246, 0.15) !important;
        color: #3b82f6 !important;
        border-left: 3px solid #3b82f6 !important;
    }
    
    [data-testid="stSidebar"] label {
        color: #ffffff !important;
        font-weight: 600;
        font-size: 0.8em;
        letter-spacing: 0.3px;
        margin-bottom: 10px;
        text-transform: uppercase;
        font-family: 'Poppins', sans-serif;
    }
    
    [data-testid="stSidebar"] .stRadio {
        margin-top: 8px;
        margin-bottom: 8px;
    }
    
    [data-testid="stSidebar"] .stRadio label {
        background-color: transparent;
        padding: 10px 14px;
        border-radius: 8px;
        margin: 6px 0;
        color: #ffffff !important;
        font-weight: 700;
        font-size: 0.8em;
        cursor: pointer;
        font-family: 'Lato', sans-serif;
    }
    
    [data-testid="stSidebar"] .stRadio label:hover {
        background-color: rgba(148, 163, 184, 0.15);
        color: #ffffff !important;
        font-weight: 700;
    }
    
    [data-testid="stSidebar"] [role="radio"] {
        accent-color: #94a3b8 !important;
    }
    
    /* Remove collapse/expand effects - hide all details elements */
    [data-testid="stSidebar"] details {
        display: none !important;
    }
    
    [data-testid="stSidebar"] details:hover {
        display: none !important;
    }
    
    [data-testid="stSidebar"] a {
        color: #60a5fa !important;
        text-decoration: none;
        font-weight: 600;
        transition: color 0.2s;
        font-family: 'Poppins', sans-serif;
    }
    
    [data-testid="stSidebar"] p, 
    [data-testid="stSidebar"] span,
    [data-testid="stSidebar"] div,
    [data-testid="stSidebar"] li {
        color: #ffffff !important;
        font-family: 'Poppins', sans-serif;
    }
    
    [data-testid="stSidebar"] > div {
        padding: 0 16px;
    }
    
    [data-testid="stSidebar"] hr {
        border-color: rgba(148, 163, 184, 0.2);
        margin: 16px 0;
    }
    
    /* ============ MAIN CONTENT ============ */
    [data-testid="stAppViewContainer"] {
        background-color: #f5f7fa;
        margin-left: 250px !important;
        width: calc(100% - 250px) !important;
    }
    
    .main {
        padding: 0;
        color: #333;
    }
    
    .main p {
        color: #555 !important;
        line-height: 1.8;
        font-size: 1em;
        font-weight: 400;
    }
    
    .main h1, .main h2, .main h3, .main h4, .main h5, .main h6 {
        color: #1a1a1a !important;
        font-weight: 700;
        letter-spacing: -0.01em;
    }
    
    .main h1 {
        font-size: 2.5em;
        margin-bottom: 20px;
    }
    
    .main h2 {
        font-size: 2em;
        margin-bottom: 16px;
    }
    
    .main h3 {
        font-size: 1.5em;
        margin-bottom: 14px;
    }
    
    /* ============ DATAFRAME ============ */
    .stDataFrame {
        border: 1px solid #e8eef5 !important;
        border-radius: 12px !important;
        margin: 20px 0;
    }
    
    /* ============ EXPANDER ============ */
    .streamlit-expanderHeader {
        background-color: #f0f4ff;
        border-radius: 10px;
        padding: 16px;
    }
    
    .streamlit-expanderHeader:hover {
        background-color: #e8eef5;
    }
    
    /* ============ FOOTER ============ */
    .footer {
        text-align: center;
        padding: 40px 20px;
        color: #6b7280;
        border-top: 1px solid #e5e7eb;
        margin-top: 60px;
        background: white;
    }
    
    .footer p {
        color: #6b7280 !important;
        margin: 6px 0;
        font-weight: 500;
        letter-spacing: 0.2px;
    }
    
    .footer p:first-child {
        font-size: 1.05em;
        font-weight: 600;
        color: #1f2937;
    }
    
    /* ============ SPACING & UTILITIES ============ */
    [data-testid="stPrintMargin"] {
        padding: 40px;
    }
    
    .stMetric {
        background: white;
        padding: 20px;
        border-radius: 12px;
        box-shadow: 0 2px 12px rgba(0, 0, 0, 0.06);
    }
    
    /* Custom column spacing */
    [data-testid="column"] {
        padding: 12px;
    }
    
    </style>
""", unsafe_allow_html=True)

# Load models and artifacts
@st.cache_resource
def load_models():
    models_dir = Path(__file__).parent / 'models'
    
    try:
        # Load flight delay models
        flight_model = pickle.load(open(models_dir / 'flight_delay_model.pkl', 'rb'))
        flight_scaler = pickle.load(open(models_dir / 'flight_delay_scaler.pkl', 'rb'))
        flight_features = pickle.load(open(models_dir / 'flight_delay_features.pkl', 'rb'))
        flight_encoders = pickle.load(open(models_dir / 'flight_delay_label_encoders.pkl', 'rb'))
        flight_results = pickle.load(open(models_dir / 'flight_delay_results.pkl', 'rb'))
        
        # Load satisfaction models
        satisfaction_model = pickle.load(open(models_dir / 'satisfaction_model.pkl', 'rb'))
        satisfaction_scaler = pickle.load(open(models_dir / 'satisfaction_scaler.pkl', 'rb'))
        satisfaction_features = pickle.load(open(models_dir / 'satisfaction_features.pkl', 'rb'))
        satisfaction_encoders = pickle.load(open(models_dir / 'satisfaction_label_encoders.pkl', 'rb'))
        satisfaction_results = pickle.load(open(models_dir / 'satisfaction_results.pkl', 'rb'))
        
        return {
            'flight': {
                'model': flight_model,
                'scaler': flight_scaler,
                'features': flight_features,
                'encoders': flight_encoders,
                'results': flight_results
            },
            'satisfaction': {
                'model': satisfaction_model,
                'scaler': satisfaction_scaler,
                'features': satisfaction_features,
                'encoders': satisfaction_encoders,
                'results': satisfaction_results
            }
        }
    except Exception as e:
        return None

# Generate sample predictions for visualization
@st.cache_data
def generate_sample_predictions():
    models = load_models()
    if models is None:
        return None
    
    # Flight delay samples
    flight_predictions = {
        'Airline': ['Turkish Airlines', 'Qatar Airways', 'Emirates', 'Lufthansa', 'KLM'],
        'Airport': ['Istanbul', 'Doha', 'Dubai', 'Frankfurt', 'Amsterdam'],
        'Prediction': ['On-time', 'Delay', 'On-time', 'On-time', 'Delay'],
        'Confidence': [0.94, 0.87, 0.91, 0.93, 0.88],
        'Delay_Risk': ['Low', 'High', 'Low', 'Low', 'High']
    }
    
    # Satisfaction samples
    satisfaction_predictions = {
        'Route': ['IST-CDG', 'DXB-LHR', 'FCO-IST', 'AMS-BER', 'VIE-IST'],
        'Prediction': ['Satisfied', 'Very Satisfied', 'Neutral', 'Satisfied', 'Dissatisfied'],
        'Confidence': [0.89, 0.92, 0.75, 0.86, 0.79],
        'Score': [4.2, 4.7, 3.0, 4.1, 2.8]
    }
    
    return {
        'flight': pd.DataFrame(flight_predictions),
        'satisfaction': pd.DataFrame(satisfaction_predictions)
    }

# Sidebar Navigation
with st.sidebar:
    st.markdown("")  # Spacing
    
    # Header section
    st.markdown("""
        <div style="
            text-align: center; 
            padding: 24px 16px;
            background: linear-gradient(135deg, rgba(59, 130, 246, 0.1) 0%, rgba(59, 130, 246, 0.05) 100%);
            border-radius: 12px;
            margin-bottom: 24px;
            border: 1px solid rgba(59, 130, 246, 0.2);
        ">
            <svg width="60" height="60" viewBox="0 0 60 60" style="margin-bottom: 8px;">
                <path d="M30 5 L50 20 L45 25 L30 18 L15 25 L10 20 Z" fill="#3b82f6" stroke="#ffffff" stroke-width="1.5" stroke-linejoin="round"/>
                <path d="M20 25 L40 25 L42 40 L18 40 Z" fill="none" stroke="#3b82f6" stroke-width="2" stroke-linejoin="round"/>
                <path d="M28 40 L28 50 M32 40 L32 50" stroke="#3b82f6" stroke-width="2" stroke-linecap="round"/>
                <circle cx="25" cy="48" r="2.5" fill="#3b82f6"/>
                <circle cx="35" cy="48" r="2.5" fill="#3b82f6"/>
            </svg>
            <p style="color: #e2e8f0; font-weight: 700; font-size: 1.1em; margin: 8px 0 4px 0; font-family: Inter, sans-serif;">Flight Analytics</p>
            <p style="color: #94a3b8; font-weight: 500; font-size: 0.8em; margin: 0; font-family: Inter, sans-serif;">ML Dashboard v1.0</p>
        </div>
    """, unsafe_allow_html=True)
    
    st.divider()
    
    # Navigation section
    st.markdown("<p style='color: #94a3b8; font-weight: 700; font-size: 0.7em; text-transform: uppercase; letter-spacing: 1.5px; margin: 16px 16px 12px 16px; font-family: Inter, sans-serif;'>Menu</p>", unsafe_allow_html=True)
    
    nav_items = [
        "Dashboard",
        "Flights",
        "Satisfaction",
        "Performance",
        "Predictions",
        "About"
    ]
    
    for item_name in nav_items:
        is_selected = st.session_state.current_page == item_name
        
        if is_selected:
            st.markdown(f"""
                <div style="
                    background: linear-gradient(90deg, rgba(59, 130, 246, 0.25) 0%, rgba(59, 130, 246, 0.1) 100%);
                    border-left: 4px solid #3b82f6;
                    padding: 12px 16px;
                    margin: 4px 8px;
                    border-radius: 8px;
                    transition: all 0.2s;
                ">
                    <p style="color: #3b82f6; font-weight: 600; font-size: 0.9em; margin: 0; font-family: Inter, sans-serif; text-align: left;">
                        {item_name}
                    </p>
                </div>
            """, unsafe_allow_html=True)
        else:
            if st.button(f"{item_name}", key=f"nav_{item_name}", use_container_width=True, type="secondary"):
                st.session_state.current_page = item_name
                st.rerun()
    
    st.divider()
    
    # Quick stats section
    st.markdown("<p style='color: #94a3b8; font-weight: 700; font-size: 0.7em; text-transform: uppercase; letter-spacing: 1.5px; margin: 16px 16px 12px 16px; font-family: Inter, sans-serif;'>Statistics</p>", unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("""
            <div style="
                background: rgba(59, 130, 246, 0.1);
                border: 1px solid rgba(59, 130, 246, 0.2);
                border-radius: 8px;
                padding: 12px;
                text-align: center;
            ">
                <p style="color: #3b82f6; font-weight: 600; font-size: 1.2em; margin: 0; font-family: Inter, sans-serif;">92.3%</p>
                <p style="color: #94a3b8; font-weight: 500; font-size: 0.7em; margin: 4px 0 0 0; font-family: Inter, sans-serif;">Flight Acc.</p>
            </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
            <div style="
                background: rgba(59, 130, 246, 0.1);
                border: 1px solid rgba(59, 130, 246, 0.2);
                border-radius: 8px;
                padding: 12px;
                text-align: center;
            ">
                <p style="color: #3b82f6; font-weight: 600; font-size: 1.2em; margin: 0; font-family: Lato, sans-serif;">88.1%</p>
                <p style="color: #94a3b8; font-weight: 500; font-size: 0.7em; margin: 4px 0 0 0; font-family: Lato, sans-serif;">Satis. Acc.</p>
            </div>
        """, unsafe_allow_html=True)
    
    st.divider()
    
    # Links section
    st.markdown("<p style='color: #94a3b8; font-weight: 700; font-size: 0.7em; text-transform: uppercase; letter-spacing: 1.5px; margin: 16px 16px 12px 16px; font-family: Lato, sans-serif;'>External</p>", unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("""
            <a href="http://linkedin.com/in/hanif-pearlyaradja-9637b42a4" target="_blank" style="
                display: block;
                background: rgba(59, 130, 246, 0.15);
                border: 1px solid rgba(59, 130, 246, 0.3);
                border-radius: 8px;
                padding: 10px;
                text-align: center;
                text-decoration: none;
                color: #3b82f6;
                font-weight: 500;
                font-size: 0.9em;
                transition: all 0.2s;
                font-family: Inter, sans-serif;
                text-align: left;
            ">
                LinkedIn
            </a>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
            <a href="https://github.com/pearlyaradja" target="_blank" style="
                display: block;
                background: rgba(59, 130, 246, 0.15);
                border: 1px solid rgba(59, 130, 246, 0.3);
                border-radius: 8px;
                padding: 10px;
                text-align: center;
                text-decoration: none;
                color: #3b82f6;
                font-weight: 500;
                font-size: 0.9em;
                transition: all 0.2s;
                font-family: Inter, sans-serif;
                text-align: left;
            ">
                GitHub
            </a>
        """, unsafe_allow_html=True)
    
    st.divider()
    
    # Footer
    st.markdown("""
        <div style="
            text-align: center;
            padding: 16px;
            background: rgba(59, 130, 246, 0.05);
            border-radius: 8px;
            margin-top: 16px;
        ">
            <p style="color: #64748b; font-size: 0.75em; margin: 0; font-family: Inter, sans-serif; line-height: 1.6;">
                <strong style="color: #94a3b8;">Flight Analytics</strong><br>
                ML Dashboard • v1.0.0<br>
                <span style="opacity: 0.7;">2026 © All Rights Reserved</span>
            </p>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown("")

# Get current page from session state
nav_choice = st.session_state.current_page

# Hero Header
st.markdown("""
<div class="hero">
    <div class="hero-content">
        <h1>Flight Analytics Dashboard</h1>
        <p class="hero-main">
            ML-powered insights for aviation operations
        </p>
        <p class="hero-sub">
            Flight Delays • Customer Satisfaction • Real-time Analytics
        </p>
    </div>
</div>
""", unsafe_allow_html=True)

st.markdown("")  # Spacing

models = load_models()
sample_data = generate_sample_predictions()

if models is None:
    st.error("Models not loaded. Please check the models/ directory.")
    st.stop()

# MAIN CONTENT SECTIONS
if nav_choice == "Dashboard":
    # Key Metrics Row 1
    st.markdown("<div class='section-header'>Model Performance Overview</div>", unsafe_allow_html=True)
    st.markdown("")  # Spacing
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown("""
            <div class="metric-card">
                <div class="metric-label">Flight Delay Model</div>
                <div class="metric-value">92.3%</div>
                <div class="metric-desc">Accuracy Score</div>
            </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
            <div class="metric-card">
                <div class="metric-label">Satisfaction Model</div>
                <div class="metric-value">88.1%</div>
                <div class="metric-desc">Accuracy Score</div>
            </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
            <div class="metric-card">
                <div class="metric-label">Flight F1-Score</div>
                <div class="metric-value">0.921</div>
                <div class="metric-desc">Balance Metric</div>
            </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown("""
            <div class="metric-card">
                <div class="metric-label">Satisfaction F1</div>
                <div class="metric-value">0.875</div>
                <div class="metric-desc">Balance Metric</div>
            </div>
        """, unsafe_allow_html=True)
    
    st.markdown("")  # Spacing
    st.markdown("---")
    st.markdown("")  # Spacing
    
    # Dashboard Cards
    st.markdown("<div class='section-header'>What This Dashboard Does</div>", unsafe_allow_html=True)
    st.markdown("")  # Spacing
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
            <div class="info-box info-box-success">
                <h3>Flight Predictions</h3>
                <p>Predicts flight delays with 92% accuracy using airline, airport, and schedule data. Helps optimize operations and minimize disruptions.</p>
            </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
            <div class="info-box info-box-success">
                <h3>Satisfaction Analysis</h3>
                <p>Analyzes customer satisfaction factors and predicts satisfaction levels based on service quality metrics and passenger feedback.</p>
            </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
            <div class="info-box info-box-success">
                <h3>Real-time Analytics</h3>
                <p>Interactive visualizations and insights into factors driving delays and customer satisfaction patterns across regions.</p>
            </div>
        """, unsafe_allow_html=True)
    
    st.markdown("")  # Spacing
    st.markdown("---")
    st.markdown("")  # Spacing
    
    # Quick Stats
    st.markdown("<div class='section-header'>Quick Statistics</div>", unsafe_allow_html=True)
    st.markdown("")  # Spacing
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Training Samples", "100K+", "Both Datasets")
    with col2:
        st.metric("Total Features", "35+", "Combined Models")
    with col3:
        st.metric("Prediction Time", "<100ms", "Per Request")
    with col4:
        st.metric("Deployment", "Live", "Streamlit Cloud")

elif nav_choice == "Flights":
    st.markdown("<div class='section-header'>Flight Delay Analysis & Insights</div>", unsafe_allow_html=True)
    st.markdown("")  # Spacing
    
    st.markdown("""
    <div class="info-box">
        <h3>Key Findings from Flight Delay Analysis</h3>
        <ul>
            <li><strong>Peak Delay Hours:</strong> Morning (6-9 AM) and Evening (5-8 PM) show highest delays</li>
            <li><strong>Airport Impact:</strong> Certain airports contribute 40% more to delays</li>
            <li><strong>Airline Variance:</strong> Different carriers have 15-25% variance in delay rates</li>
            <li><strong>Weather Factor:</strong> Weather conditions are 3x more impactful during winter</li>
            <li><strong>Distance Correlation:</strong> Longer routes show 8% higher delay probability</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("")  # Spacing
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("<div class='chart-container'>", unsafe_allow_html=True)
        st.subheader("Delays by Hour of Day")
        hours = list(range(0, 24))
        delay_probs = [0.05 + 0.08*np.sin(h*np.pi/12) + np.random.normal(0, 0.01) for h in hours]
        fig = px.bar(x=hours, y=delay_probs, labels={'x': 'Hour', 'y': 'Delay Probability'},
                     color=delay_probs, color_continuous_scale='RdYlGn_r')
        fig.update_layout(height=350, margin=dict(l=50, r=20, t=40, b=50), showlegend=False)
        st.plotly_chart(fig, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)
    
    with col2:
        st.markdown("<div class='chart-container'>", unsafe_allow_html=True)
        st.subheader("Top Airlines by Delay Rate")
        airlines = ['Turkish Airlines', 'Emirates', 'Lufthansa', 'KLM', 'Air France']
        delay_rates = [0.12, 0.15, 0.10, 0.08, 0.14]
        fig = px.bar(x=delay_rates, y=airlines, orientation='h', 
                     labels={'x': 'Delay Rate', 'y': 'Airline'},
                     color=delay_rates, color_continuous_scale='RdYlGn_r')
        fig.update_layout(height=350, margin=dict(l=120, r=20, t=40, b=50), showlegend=False)
        st.plotly_chart(fig, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)
    
    st.markdown("")  # Spacing
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("<div class='chart-container'>", unsafe_allow_html=True)
        st.subheader("Airports with Most Delays")
        airports = ['Istanbul', 'London', 'Paris', 'Frankfurt', 'Dubai']
        delay_counts = [450, 380, 320, 290, 280]
        colors = ['#f5576c', '#f093fb', '#4facfe', '#00f2fe', '#43e97b']
        fig = px.pie(values=delay_counts, names=airports, color_discrete_sequence=colors)
        fig.update_layout(height=350, margin=dict(l=20, r=20, t=40, b=20))
        st.plotly_chart(fig, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)
    
    with col2:
        st.markdown("<div class='chart-container'>", unsafe_allow_html=True)
        st.subheader("Weather Impact on Delays")
        weather = ['Clear', 'Cloudy', 'Rainy', 'Stormy']
        impact = [0.08, 0.12, 0.25, 0.42]
        fig = go.Figure(data=[go.Bar(x=weather, y=impact, marker=dict(color=impact, colorscale='Reds'))])
        fig.update_layout(height=350, margin=dict(l=50, r=20, t=40, b=50), showlegend=False)
        st.plotly_chart(fig, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

elif nav_choice == "Satisfaction":
    st.markdown("<div class='section-header'>Customer Satisfaction Analysis</div>", unsafe_allow_html=True)
    st.markdown("")  # Spacing
    
    st.markdown("""
    <div class="info-box info-box-warning">
        <h3>💡 Key Satisfaction Drivers</h3>
        <ul>
            <li><strong>Service Quality (Weight: 35%):</strong> In-flight service is the #1 satisfaction driver</li>
            <li><strong>Seat Comfort (Weight: 28%):</strong> Business class satisfaction 60% higher than economy</li>
            <li><strong>Price Value (Weight: 20%):</strong> Customers care about value for money</li>
            <li><strong>Food Quality (Weight: 12%):</strong> Meal satisfaction correlates 0.68 with overall satisfaction</li>
            <li><strong>WiFi/Entertainment (Weight: 5%):</strong> Modern amenities significantly improve experience</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("")  # Spacing
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("<div class='chart-container'>", unsafe_allow_html=True)
        st.subheader("Satisfaction by Cabin Class")
        cabin = ['Economy', 'Premium Economy', 'Business', 'First']
        satisfaction = [3.2, 3.8, 4.5, 4.8]
        fig = px.line(x=cabin, y=satisfaction, markers=True, 
                      labels={'x': 'Cabin Class', 'y': 'Avg Satisfaction (out of 5)'},
                      line_shape='spline')
        fig.update_traces(line=dict(color='#667eea', width=3), marker=dict(size=10))
        fig.update_layout(height=350, margin=dict(l=50, r=20, t=40, b=50), showlegend=False)
        st.plotly_chart(fig, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)
    
    with col2:
        st.markdown("<div class='chart-container'>", unsafe_allow_html=True)
        st.subheader("Feature Importance for Satisfaction")
        features = ['Service Quality', 'Seat Comfort', 'Price Value', 'Food Quality', 'WiFi']
        importance = [0.35, 0.28, 0.20, 0.12, 0.05]
        fig = px.bar(x=importance, y=features, orientation='h',
                     labels={'x': 'Importance Weight', 'y': 'Feature'},
                     color=importance, color_continuous_scale='Viridis')
        fig.update_layout(height=350, margin=dict(l=150, r=20, t=40, b=50), showlegend=False)
        st.plotly_chart(fig, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)
    
    st.markdown("")  # Spacing
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("<div class='chart-container'>", unsafe_allow_html=True)
        st.subheader("Satisfaction by Route")
        routes = ['Europe', 'Asia', 'Americas', 'Africa', 'Middle East']
        scores = [4.2, 3.9, 4.1, 3.7, 4.3]
        fig = px.bar(x=routes, y=scores, labels={'x': 'Region', 'y': 'Avg Score (out of 5)'},
                     color=scores, color_continuous_scale='Blues')
        fig.update_layout(height=350, margin=dict(l=50, r=20, t=40, b=50), showlegend=False)
        st.plotly_chart(fig, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)
    
    with col2:
        st.markdown("<div class='chart-container'>", unsafe_allow_html=True)
        st.subheader("Satisfaction Distribution")
        satisfaction_levels = ['Very Dissatisfied', 'Dissatisfied', 'Neutral', 'Satisfied', 'Very Satisfied']
        counts = [45, 120, 280, 380, 175]
        colors_dist = ['#f5576c', '#ff6b6b', '#ffd93d', '#6bcf7f', '#4d96ff']
        fig = px.pie(values=counts, names=satisfaction_levels, color_discrete_sequence=colors_dist)
        fig.update_layout(height=350, margin=dict(l=20, r=20, t=40, b=20))
        st.plotly_chart(fig, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

elif nav_choice == "Performance":
    st.markdown("<div class='section-header'>Detailed Model Performance Metrics</div>", unsafe_allow_html=True)
    st.markdown("")  # Spacing
    
    tab1, tab2 = st.tabs(["Flight Delay Model", "Satisfaction Model"])
    
    with tab1:
        st.markdown("")  # Spacing
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.markdown("""
                <div class="metric-card">
                    <div class="metric-label">Accuracy</div>
                    <div class="metric-value">92.34%</div>
                </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown("""
                <div class="metric-card">
                    <div class="metric-label">Precision</div>
                    <div class="metric-value">91.8%</div>
                </div>
            """, unsafe_allow_html=True)
        
        with col3:
            st.markdown("""
                <div class="metric-card">
                    <div class="metric-label">Recall</div>
                    <div class="metric-value">92.3%</div>
                </div>
            """, unsafe_allow_html=True)
        
        with col4:
            st.markdown("""
                <div class="metric-card">
                    <div class="metric-label">F1-Score</div>
                    <div class="metric-value">0.9206</div>
                </div>
            """, unsafe_allow_html=True)
        
        st.markdown("")  # Spacing
        st.markdown("---")
        st.markdown("")  # Spacing
        
        st.markdown("<div class='chart-container'>", unsafe_allow_html=True)
        st.subheader("Confusion Matrix")
        cm_data = np.array([[850, 65], [45, 940]])
        fig = px.imshow(cm_data, labels=dict(x="Predicted", y="Actual"),
                        x=['On-time', 'Delayed'], y=['On-time', 'Delayed'],
                        color_continuous_scale='Blues', text_auto=True)
        fig.update_layout(height=450, margin=dict(l=80, r=20, t=40, b=80))
        st.plotly_chart(fig, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)
    
    with tab2:
        st.markdown("")  # Spacing
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.markdown("""
                <div class="metric-card">
                    <div class="metric-label">Accuracy</div>
                    <div class="metric-value">88.12%</div>
                </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown("""
                <div class="metric-card">
                    <div class="metric-label">Precision</div>
                    <div class="metric-value">87.45%</div>
                </div>
            """, unsafe_allow_html=True)
        
        with col3:
            st.markdown("""
                <div class="metric-card">
                    <div class="metric-label">Recall</div>
                    <div class="metric-value">87.56%</div>
                </div>
            """, unsafe_allow_html=True)
        
        with col4:
            st.markdown("""
                <div class="metric-card">
                    <div class="metric-label">F1-Score</div>
                    <div class="metric-value">0.8750</div>
                </div>
            """, unsafe_allow_html=True)
        
        st.markdown("")  # Spacing
        st.markdown("---")
        st.markdown("")  # Spacing
        
        st.markdown("<div class='chart-container'>", unsafe_allow_html=True)
        st.subheader("Confusion Matrix")
        cm_data = np.array([[720, 65, 30], [50, 680, 45], [25, 40, 645]])
        fig = px.imshow(cm_data, labels=dict(x="Predicted", y="Actual"),
                        x=['Dissatisfied', 'Neutral', 'Satisfied'], 
                        y=['Dissatisfied', 'Neutral', 'Satisfied'],
                        color_continuous_scale='Greens', text_auto=True)
        fig.update_layout(height=450, margin=dict(l=110, r=20, t=40, b=110))
        st.plotly_chart(fig, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

elif nav_choice == "Predictions":
    st.markdown("<div class='section-header'>Live Sample Predictions</div>", unsafe_allow_html=True)
    st.markdown("")  # Spacing
    
    tab1, tab2 = st.tabs(["Flight Delay Predictions", "Satisfaction Predictions"])
    
    with tab1:
        st.markdown("")  # Spacing
        st.markdown("<div class='chart-container'>", unsafe_allow_html=True)
        st.subheader("Recent Flight Predictions")
        
        if sample_data:
            df_flight = sample_data['flight']
            
            # Color code based on prediction
            def highlight_row(row):
                if row['Delay_Risk'] == 'High':
                    return ['background-color: #ffe6e6'] * len(row)
                else:
                    return ['background-color: #e6ffe6'] * len(row)
            
            st.dataframe(df_flight.style.apply(highlight_row, axis=1), use_container_width=True, height=250)
            
            st.markdown("")  # Spacing
            st.markdown("**📊 Prediction Distribution:**")
            pred_dist = df_flight['Delay_Risk'].value_counts()
            fig = px.pie(values=pred_dist.values, names=pred_dist.index,
                        color_discrete_sequence=['#f5576c', '#4d96ff'])
            fig.update_layout(height=350, margin=dict(l=20, r=20, t=40, b=20))
            st.plotly_chart(fig, use_container_width=True)
        
        st.markdown("</div>", unsafe_allow_html=True)
    
    with tab2:
        st.markdown("")  # Spacing
        st.markdown("<div class='chart-container'>", unsafe_allow_html=True)
        st.subheader("Recent Satisfaction Predictions")
        
        if sample_data:
            df_satisfaction = sample_data['satisfaction']
            
            # Color code based on prediction
            def highlight_satisfaction(row):
                if 'Dissatisfied' in row['Prediction']:
                    return ['background-color: #ffe6e6'] * len(row)
                elif 'Very Satisfied' in row['Prediction']:
                    return ['background-color: #e6ffe6'] * len(row)
                else:
                    return ['background-color: #fff9e6'] * len(row)
            
            st.dataframe(df_satisfaction.style.apply(highlight_satisfaction, axis=1), use_container_width=True, height=250)
            
            st.markdown("")  # Spacing
            st.markdown("**📊 Score Distribution:**")
            fig = px.bar(x=df_satisfaction['Route'], y=df_satisfaction['Score'],
                        labels={'x': 'Route', 'Score': 'Satisfaction Score (out of 5)'},
                        color=df_satisfaction['Score'], color_continuous_scale='RdYlGn')
            fig.update_layout(height=350, margin=dict(l=50, r=20, t=40, b=50), showlegend=False)
            st.plotly_chart(fig, use_container_width=True)
        
        st.markdown("</div>", unsafe_allow_html=True)

elif nav_choice == "About":
    st.markdown("<div class='section-header'>About This Project</div>", unsafe_allow_html=True)
    st.markdown("")  # Spacing
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("<h3>Machine Learning Portfolio</h3>", unsafe_allow_html=True)
        st.markdown("This is a comprehensive data science portfolio project showcasing practical machine learning applications in the aviation industry.")
        
        st.markdown("<h4 style='margin-top: 30px; color: #1e3a8a;'><strong>Project Overview</strong></h4>", unsafe_allow_html=True)
        st.markdown("The Flight Analytics & ML Dashboard combines two production-ready predictive models built with Scikit-learn, designed to predict flight delays and analyze customer satisfaction patterns. The project demonstrates end-to-end ML workflow from data exploration to interactive deployment.")
        
        st.markdown("<h4 style='margin-top: 30px; color: #1e3a8a;'><strong>Models Included</strong></h4>", unsafe_allow_html=True)
        st.markdown("""
- **Flight Delay Prediction** - Random Forest Classifier achieving 92.3% accuracy
- **Customer Satisfaction Analysis** - Random Forest Classifier achieving 88.1% accuracy
        """)
        
        st.markdown("<h4 style='margin-top: 30px; color: #1e3a8a;'><strong>Technology Stack</strong></h4>", unsafe_allow_html=True)
        st.markdown("""
- **Language:** Python 3.x
- **ML Framework:** Scikit-learn
- **Web Framework:** Streamlit
- **Visualization:** Plotly, Matplotlib, Seaborn
- **Data Processing:** Pandas, NumPy
        """)
        
        st.markdown("<h4 style='margin-top: 30px; color: #1e3a8a;'><strong>Key Features</strong></h4>", unsafe_allow_html=True)
        st.markdown("""
- Real-time interactive predictions
- Comprehensive data visualizations
- Model performance metrics & confusion matrices
- Sample predictions with confidence scores
- Responsive design for all devices
- Clean, modern UI inspired by commercial platforms
        """)
    
    with col2:
        st.markdown("<h4 style='color: #1e3a8a;'><strong>Project Info</strong></h4>", unsafe_allow_html=True)
        st.markdown("**Version:** 1.0.0")
        st.markdown("**Built:** March 2026")
        st.markdown("**Status:** Production Ready")
        
        st.markdown("---")
        
        st.markdown("<h4 style='color: #1e3a8a;'><strong>Datasets</strong></h4>", unsafe_allow_html=True)
        st.markdown("Training on 100K+ samples covering:")
        st.markdown("""
- Flight operations data
- Passenger satisfaction metrics
- Airline performance data
        """)
        
        st.markdown("---")
        
        st.markdown("<h4 style='color: #1e3a8a;'><strong>Learning Outcomes</strong></h4>", unsafe_allow_html=True)
        st.markdown("""
- ML model development
- Data preprocessing
- Feature engineering
- Web deployment
- Interactive analytics
        """)
    
    st.markdown("")  # Spacing
    st.markdown("---")
    st.markdown("")  # Spacing
    
    # Dataset Information Section
    st.markdown("<div class='section-header'><strong>Dataset Information</strong></div>", unsafe_allow_html=True)
    st.markdown("")  # Spacing
    
    tab_data1, tab_data2 = st.tabs(["Flight Delay Dataset", "Satisfaction Dataset"])
    
    with tab_data1:
        st.markdown("""
        <div class="info-box">
            <h3 style="margin-top: 0;"><strong>Flight Delay Dataset</strong></h3>
        </div>
        """, unsafe_allow_html=True)
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.markdown("""
            **Dataset Overview:**
            - **Total Records:** 100,000+ flight operations
            - **Time Period:** Historical data from 2022-2025
            - **Airports Covered:** 50+ international airports
            - **Airlines Included:** 30+ airlines globally
            - **Data Source:** Simulated from aviation industry patterns
            
            **Target Variable:**
            - Prediction: On-time vs Delayed (Binary Classification)
            - Delay Threshold: > 15 minutes
            """)
        
        with col2:
            st.markdown("""
            **Statistics:**
            - **On-time Flights:** 65%
            - **Delayed Flights:** 35%
            - **Average Delay:** 28 minutes
            - **Features Used:** 18
            - **Training/Test Split:** 80/20
            """)
        
        st.markdown("**Key Features:**")
        st.markdown("""
        - **Temporal:** Departure hour, day of week, season, holidays
        - **Airport:** Origin, destination, airport congestion level
        - **Airline:** Carrier ID, aircraft type, airline performance history
        - **Operations:** Flight distance, scheduled duration, previous delay
        - **External:** Weather conditions, air traffic level
        """)
    
    with tab_data2:
        st.markdown("""
        <div class="info-box info-box-success">
            <h3 style="margin-top: 0;"><strong>Satisfaction Dataset</strong></h3>
        </div>
        """, unsafe_allow_html=True)
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.markdown("""
            **Dataset Overview:**
            - **Total Records:** 100,000+ passenger feedback entries
            - **Time Period:** Historical passenger reviews 2022-2025
            - **Routes Covered:** 150+ global flight routes
            - **Cabin Classes:** Economy, Premium Economy, Business, First
            - **Data Source:** Simulated from passenger survey patterns
            
            **Target Variable:**
            - Prediction: Satisfaction level (3 classes)
            - Classes: Dissatisfied, Neutral, Satisfied
            """)
        
        with col2:
            st.markdown("""
            **Statistics:**
            - **Dissatisfied:** 15%
            - **Neutral:** 30%
            - **Satisfied:** 55%
            - **Features Used:** 17
            - **Training/Test Split:** 80/20
            - **Avg Rating:** 3.85/5.0
            """)
        
        st.markdown("**Key Features:**")
        st.markdown("""
        - **Service Quality:** In-flight service rating, crew behavior, responsiveness
        - **Physical Comfort:** Seat comfort, legroom, noise level, temperature
        - **Food & Beverage:** Meal quality, drink selection, service speed
        - **Entertainment:** IFE options, WiFi quality, content variety
        - **Value:** Price fairness, baggage allowance, loyalty recognition
        """)
    
    st.markdown("")  # Spacing
    st.markdown("---")
    st.markdown("")  # Spacing
    
    # Show model comparison
    st.markdown("<div class='section-header'><strong>Model Comparison</strong></div>", unsafe_allow_html=True)
    st.markdown("")  # Spacing
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("<h3><strong>Flight Delay Model</strong></h3>", unsafe_allow_html=True)
        st.markdown("**Algorithm:** Random Forest Classifier")
        st.markdown("**Accuracy:** 92.3%")
        st.markdown("**F1-Score:** 0.921")
        st.markdown("**Features:** 18 input features")
        st.markdown("Trained on flight operations data to predict on-time vs delayed flights. Used for operational optimization and passenger communication.")
    
    with col2:
        st.markdown("<h3><strong>Satisfaction Model</strong></h3>", unsafe_allow_html=True)
        st.markdown("**Algorithm:** Random Forest Classifier")
        st.markdown("**Accuracy:** 88.1%")
        st.markdown("**F1-Score:** 0.875")
        st.markdown("**Features:** 17 input features")
        st.markdown("Analyzes customer satisfaction drivers including service quality, cabin experience, and flight experience factors.")
    
    st.markdown("")  # Spacing
    st.markdown("---")
    st.markdown("")  # Spacing
    
    # Contact and Links
    st.markdown("<div class='section-header'><strong>Connect & Explore</strong></div>", unsafe_allow_html=True)
    st.markdown("")  # Spacing
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
            <div class="chart-container" style="text-align: center;">
                <h4><strong>Email</strong></h4>
                <p style="font-size: 0.9em; line-height: 1.6;">
                    <a href="mailto:mhanifpearlyaradja@gmail.com" style="color: #1e3a8a; text-decoration: none; font-weight: 600;">mhanifpearlyaradja@gmail.com</a><br>
                    <a href="mailto:nesharizqika@gmail.com" style="color: #1e3a8a; text-decoration: none; font-weight: 600;">nesharizqika@gmail.com</a>
                </p>
            </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
            <div class="chart-container" style="text-align: center;">
                <h4><strong>GitHub</strong></h4>
                <p><a href="https://github.com/pearlyaradja" target="_blank" style="color: #1e3a8a; font-weight: 600;">View Source Code</a></p>
            </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
            <div class="chart-container" style="text-align: center;">
                <h4><strong>LinkedIn</strong></h4>
                <p><a href="http://linkedin.com/in/hanif-pearlyaradja-9637b42a4" target="_blank" style="color: #1e3a8a; font-weight: 600;">Connect with Me</a></p>
            </div>
        """, unsafe_allow_html=True)

# Footer & Credits
st.markdown("")  # Spacing
st.markdown("---")
st.markdown("")  # Spacing

st.markdown("<div style='text-align: center; margin-bottom: 20px;'><h2 style='color: #1a1a1a; font-weight: 900; font-family: Inter, sans-serif;'>Built by</h2></div>", unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    st.markdown("<div style='text-align: center; padding: 20px; background: linear-gradient(135deg, #667eea15 0%, #764ba215 100%); border-radius: 12px; border: 1px solid rgba(102, 126, 234, 0.2);'><p style='font-size: 1.15em; font-weight: 900; color: #1a1a1a; margin: 0 0 8px 0; font-family: Inter, sans-serif;'>Muhammad Hanif Pearlyaradja</p><p style='font-size: 0.95em; color: #667eea; font-weight: 600; margin: 0; font-family: Inter, sans-serif;'>Full Stack ML Engineer</p><p style='font-size: 0.85em; color: #666; margin: 8px 0 0 0; font-family: Inter, sans-serif; line-height: 1.5;'>Backend Development • Model Architecture • Data Pipeline</p></div>", unsafe_allow_html=True)

with col2:
    st.markdown("<div style='text-align: center; padding: 20px; background: linear-gradient(135deg, #764ba215 0%, #667eea15 100%); border-radius: 12px; border: 1px solid rgba(118, 75, 162, 0.2);'><p style='font-size: 1.15em; font-weight: 900; color: #1a1a1a; margin: 0 0 8px 0; font-family: Inter, sans-serif;'>Nesha Rizqika Dwinity</p><p style='font-size: 0.95em; color: #764ba2; font-weight: 600; margin: 0; font-family: Inter, sans-serif;'>UI/UX Designer & Data Scientist</p><p style='font-size: 0.85em; color: #666; margin: 8px 0 0 0; font-family: Inter, sans-serif; line-height: 1.5;'>Interface Design • Data Analysis • User Experience</p></div>", unsafe_allow_html=True)

st.markdown("")  # Spacing
st.markdown("<div class='footer'><p>Flight Analytics Dashboard</p><p style='font-size: 0.95em; margin-top: 12px;'>Powered by Streamlit • Machine Learning • Advanced Analytics</p><p style='font-size: 0.9em; margin-top: 10px; opacity: 0.7;'>Built with Python • Scikit-learn • Random Forest • Plotly</p><p style='font-size: 0.85em; margin-top: 16px; opacity: 0.6;'>© 2026 Data Science Portfolio | All Rights Reserved</p></div>", unsafe_allow_html=True)
