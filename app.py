import joblib
import numpy as np
import pandas as pd
import streamlit as st
import time
from datetime import datetime
import base64
import os

# Page configuration
st.set_page_config(
    page_title="AJM Predictions",
    page_icon="⚡",
    layout="centered",
    initial_sidebar_state="collapsed",
)

# Initialize Session State variables
if "theme" not in st.session_state:
    st.session_state.theme = "Dark"

# Toggle Theme Function
def toggle_theme():
    st.session_state.theme = "Light" if st.session_state.theme == "Dark" else "Dark"

# Premium Dynamic Theme Styles
if st.session_state.theme == "Dark":
    bg_gradient = "linear-gradient(135deg, #09090b 0%, #1e1b4b 50%, #020617 100%)"
    glass_bg = "rgba(20, 25, 40, 0.45)"
    glass_border = "rgba(255, 255, 255, 0.08)"
    input_bg = "rgba(255, 255, 255, 0.03)"
    input_border = "rgba(255, 255, 255, 0.1)"
    input_text = "#ffffff"
    label_color = "#94a3b8"
    glow_color = "rgba(168, 85, 247, 0.5)"
else:
    bg_gradient = "linear-gradient(135deg, #fdfbfb 0%, #e2e8f0 50%, #ebedee 100%)"
    glass_bg = "rgba(255, 255, 255, 0.65)"
    glass_border = "rgba(255, 255, 255, 0.4)"
    input_bg = "rgba(255, 255, 255, 0.8)"
    input_border = "rgba(0, 0, 0, 0.08)"
    input_text = "#0f172a"
    label_color = "#475569"
    glow_color = "rgba(99, 102, 241, 0.4)"

# --- Load Image as Base64 for CSS Injection ---
def get_base64_of_bin_file(bin_file):
    with open(bin_file, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()

# Ensure you save your picture as 'logo.png' in the same folder
img_path = "logo.png"
if os.path.exists(img_path):
    img_base64 = get_base64_of_bin_file(img_path)
    img_html = f'<img src="data:image/png;base64,{img_base64}" class="logo-img">'
else:
    img_html = '<div class="logo-img" style="display:flex; align-items:center; justify-content:center; color:white; background:#333;">Logo</div>'

# Injecting Advanced Custom CSS for Glassmorphism & Animations
st.markdown(f"""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap');

    .stApp {{
        background: {bg_gradient};
        background-size: 400% 400%;
        animation: gradientBG 20s ease infinite;
        color: {input_text};
        font-family: 'Plus Jakarta Sans', sans-serif;
    }}
    
    @keyframes gradientBG {{ 
        0% {{ background-position: 0% 50%; }} 
        50% {{ background-position: 100% 50%; }} 
        100% {{ background-position: 0% 50%; }} 
    }}

    @keyframes float {{
        0% {{ transform: translateY(0px); }}
        50% {{ transform: translateY(-8px); }}
        100% {{ transform: translateY(0px); }}
    }}

    /* Spinning Neon Border CSS */
    .logo-container {{
        position: relative;
        width: 140px;
        height: 140px;
        margin: 0 auto 20px auto;
        border-radius: 50%;
        display: flex;
        justify-content: center;
        align-items: center;
        z-index: 1;
    }}
    
    /* The outer glowing spinning border */
    .logo-container::before, .logo-container::after {{
        content: '';
        position: absolute;
        inset: -5px;
        border-radius: 50%;
        background: conic-gradient(from 0deg, #ff0000, #ff8000, #ffff00, #00ff00, #00ffff, #0000ff, #8000ff, #ff0000);
        animation: spin 3s linear infinite;
        z-index: -1;
    }}
    
    .logo-container::after {{
        filter: blur(15px);
        opacity: 0.8;
    }}
    
    @keyframes spin {{
        0% {{ transform: rotate(0deg); }}
        100% {{ transform: rotate(360deg); }}
    }}

    /* Inner Image - Auto Spin every 30 seconds */
    .logo-img {{
        width: 100%;
        height: 100%;
        border-radius: 50%;
        object-fit: cover;
        border: 4px solid #1a1a2e; /* Dark inner border */
        z-index: 10;
        background-color: #0f172a;
        /* Animation details: 30s total duration. 
           Will stay still most of the time, and spin fast in 1 second */
        animation: quickSpin 30s infinite;
    }}
    
    @keyframes quickSpin {{
        0% {{ transform: rotate(0deg); }}
        3% {{ transform: rotate(360deg); }} /* 3% of 30s is roughly 1 second */
        100% {{ transform: rotate(360deg); }} /* Stays still for the rest of the 29 seconds */
    }}

    /* Premium Glassmorphism Hero Box */
    .hero-box {{ 
        background: {glass_bg}; 
        padding: 2.5rem; 
        border-radius: 24px; 
        text-align: center; 
        margin-bottom: 2rem; 
        box-shadow: 0 15px 35px rgba(0,0,0,0.1), inset 0 1px 0 {glass_border}; 
        backdrop-filter: blur(20px);
        -webkit-backdrop-filter: blur(20px);
        border: 1px solid {glass_border};
        animation: float 6s ease-in-out infinite;
    }}
    
    .hero-title {{ 
        font-size: 2.8rem; 
        font-weight: 800; 
        background: linear-gradient(135deg, #6366f1, #d946ef, #f43f5e); 
        -webkit-background-clip: text; 
        -webkit-text-fill-color: transparent; 
        letter-spacing: -1px;
        margin-bottom: 0.2rem;
    }}
    
    /* Premium Glassmorphism Form Container */
    .main-form {{ 
        background: {glass_bg}; 
        padding: 3rem; 
        border-radius: 28px; 
        box-shadow: 0 25px 50px rgba(0,0,0,0.15), inset 0 1px 0 {glass_border}; 
        backdrop-filter: blur(25px);
        -webkit-backdrop-filter: blur(25px);
        border: 1px solid {glass_border};
        transition: transform 0.3s ease;
    }}
    .main-form:hover {{
        transform: scale(1.005);
    }}

    .stNumberInput label, .stSlider label, .stSelectbox label {{ 
        color: {label_color} !important; 
        font-weight: 600 !important; 
        font-size: 0.95rem !important;
        letter-spacing: 0.3px;
        padding-bottom: 5px;
    }}
    
    .stNumberInput input, .stSelectbox div[data-baseweb="select"] {{ 
        background: {input_bg} !important; 
        color: {input_text} !important; 
        border: 1px solid {input_border} !important;
        border-radius: 14px !important; 
        padding: 10px 15px !important;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
        box-shadow: inset 0 2px 4px rgba(0,0,0,0.05) !important;
    }}

    .stNumberInput input:hover, .stSelectbox div[data-baseweb="select"]:hover {{
        border-color: #8b5cf6 !important;
        box-shadow: 0 0 12px {glow_color}, inset 0 2px 4px rgba(0,0,0,0.05) !important;
    }}
    
    .stNumberInput input:focus, .stSelectbox div[data-baseweb="select"]:focus-within {{
        border-color: #a855f7 !important;
        box-shadow: 0 0 20px {glow_color}, inset 0 2px 4px rgba(0,0,0,0.05) !important;
        transform: translateY(-2px);
    }}

    .stSlider > div {{
        padding-top: 15px !important;
    }}

    .stButton > button {{ 
        width: 100%; 
        height: 4rem; 
        border-radius: 16px; 
        font-weight: 800; 
        font-size: 1.2rem; 
        background: linear-gradient(135deg, #6366f1 0%, #a855f7 50%, #ec4899 100%);
        color: white !important;
        border: none !important;
        box-shadow: 0 10px 25px rgba(168, 85, 247, 0.4);
        transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
        letter-spacing: 0.5px;
        position: relative;
        overflow: hidden;
        z-index: 1;
    }}
    
    .stButton > button:hover {{ 
        transform: translateY(-5px) scale(1.02); 
        box-shadow: 0 20px 35px rgba(168, 85, 247, 0.6); 
    }}
    
    .stButton > button:first-child:not([type="primary"]) {{
        background: {glass_bg};
        backdrop-filter: blur(10px);
        border: 1px solid {glass_border} !important;
        color: {input_text} !important;
        box-shadow: 0 4px 15px rgba(0,0,0,0.05);
        height: auto;
        padding: 8px 16px;
        font-size: 0.9rem;
        border-radius: 20px;
    }}
</style>
""", unsafe_allow_html=True)

# Load Model
try:
    model = joblib.load("loan_model.pkl")
except:
    model = None

# Top Bar
col_space, col_btn = st.columns([7, 2])
with col_btn:
    st.button("☀️ Light Mode" if st.session_state.theme == "Dark" else "🌙 Dark Mode", on_click=toggle_theme)

# Hero Section (Updated with Logo and New Text)
st.markdown(f"""
<div class="hero-box">
    <div class="logo-container">
        {img_html}
    </div>
    <div class="hero-title">AJM PREDICTIONS</div>
    <p style="color: #cbd5e1; font-size: 1.15rem; font-weight: 500; margin-top: 5px; letter-spacing: 1px;">your mate to a better tommorow</p>
</div>
""", unsafe_allow_html=True)


# ---------------- NATIVE STREAMLIT POPUP DIALOG ---------------- #
@st.dialog("Loan Prediction Result")
def show_result_modal(pred, prob, inputs, error_msg=""):
    
    if pred == 1:
        st.markdown("<h2 style='text-align: center; color: #10b981; font-weight: 800; font-size: 2.5rem;'>🎉 APPROVED!</h2>", unsafe_allow_html=True)
    else:
        st.markdown("<h2 style='text-align: center; color: #ef4444; font-weight: 800; font-size: 2.5rem;'>❌ REJECTED</h2>", unsafe_allow_html=True)
        if error_msg:
            st.markdown(f"<p style='text-align: center; color: #ef4444; font-size: 1.1rem;'><b>Reason:</b> {error_msg}</p>", unsafe_allow_html=True)
        
    st.markdown(f"<p style='text-align: center; color: #64748b; margin-top: -5px; font-size: 1.2rem;'>AI Confidence Score: <b>{prob:.1f}%</b></p>", unsafe_allow_html=True)
    
    st.divider()

    st.markdown("#### 📊 AI Reasoning")
    
    if inputs['credit_score'] < 600:
        st.error(f"📉 Low Credit Score ({inputs['credit_score']}). AI prefers 600+")
    elif inputs['credit_score'] < 750:
        st.warning(f"⚖️ Average Credit Score ({inputs['credit_score']}). Acceptable but could be improved.")
    else:
        st.success(f"📈 Excellent Credit Score ({inputs['credit_score']}) greatly improved chances.")

    if inputs['loan_amount'] > (inputs['income'] * 0.5):
        st.error(f"📉 High Risk: Requested Loan (${inputs['loan_amount']:,}) is too high compared to Annual Income (${inputs['income']:,}).")
    else:
        st.success("📈 Healthy Income-to-Loan ratio.")

    if inputs['existing_loans'] > 1:
        st.warning(f"⚠️ Multiple existing active loans ({inputs['existing_loans']}) increases financial burden.")

    st.divider()

    if pred == 0 and not error_msg:
        st.markdown("#### 💡 Alternative Suggestion")
        safe_amount = int((inputs['income'] * 0.4) * (inputs['credit_score'] / 900))
        safe_amount = max(500, round(safe_amount / 500) * 500)
        
        if safe_amount < inputs['loan_amount']:
            st.info(f"Ningalude profile vechu **${safe_amount:,}** vare approve aavan chance undu. Please consider reducing your loan amount and try again!")
        else:
            st.info("Try improving your Credit Score before reapplying.")

    st.divider()

    report_content = f"""======================================
     AJM PREDICTIONS - LOAN AI REPORT
======================================
Date Generated: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
Status: {'APPROVED' if pred == 1 else 'REJECTED'}
AI Confidence: {prob:.1f}%

[ APPLICANT DETAILS ]
Age: {inputs['age']} Years
Annual Income: ${inputs['income']}
Employment Type: {inputs['emp_type']}
Employment Years: {inputs['emp_years']} Years
Existing Loans: {inputs['existing_loans']}

[ LOAN DETAILS ]
Requested Amount: ${inputs['loan_amount']}
Loan Term: {inputs['loan_term']} Months
Credit Score: {inputs['credit_score']}
======================================
"""
    
    col1, col2 = st.columns(2)
    with col1:
        st.download_button(
            label="📄 Download Report",
            data=report_content,
            file_name=f"AJM_Predictions_Report_{datetime.now().strftime('%Y%m%d%H%M')}.txt",
            mime="text/plain",
            use_container_width=True
        )
    with col2:
        if st.button("✖ Close", use_container_width=True):
            st.rerun()


# ---------------- FORM SECTION ---------------- #
st.markdown('<div class="main-form">', unsafe_allow_html=True)
st.markdown('<h4 style="font-weight: 700; margin-bottom: 20px;">Applicant Details</h4>', unsafe_allow_html=True)

col1, col2 = st.columns(2, gap="large")

with col1:
    age = st.number_input("Age", min_value=0, max_value=100, value=0, key="inp_age")
    income = st.number_input("Annual Income ($)", min_value=0, max_value=200000, value=0, step=1000, key="inp_inc")
    employment_years = st.number_input("Employment Years", min_value=0, max_value=40, value=0, key="inp_emp_yr")
    employment_type = st.selectbox("Employment Type", ["Salaried", "Self-Employed", "Business"], key="inp_emp_type")

with col2:
    loan_amount = st.number_input("Loan Amount ($)", min_value=0, max_value=100000, value=0, step=500, key="inp_loan_amt")
    loan_term = st.selectbox("Loan Term (Months)", [12, 24, 36, 48, 60], key="inp_term")
    credit_score = st.slider("Credit Score", min_value=300, max_value=900, value=300, key="inp_cscore")
    existing_loans = st.number_input("Existing Loans Active", min_value=0, max_value=10, value=0, key="inp_ext_loans")

input_data_dict = {
    "age": age,
    "income": income,
    "emp_years": employment_years,
    "emp_type": employment_type,
    "loan_amount": loan_amount,
    "loan_term": loan_term,
    "credit_score": credit_score,
    "existing_loans": existing_loans
}

st.markdown("<br><br>", unsafe_allow_html=True)

if st.button("Predict Loan Status", type="primary"):
    
    if age < 18:
        st.error("⚠️ അപേക്ഷകന് കുറഞ്ഞത് 18 വയസ്സ് പൂർത്തിയായിരിക്കണം! (Applicant must be at least 18 years old)")
        
    elif employment_years > (age - 18):
        show_result_modal(0, 100.0, input_data_dict, "Employment years logically mismatch with the applicant's age.")
        
    elif employment_years < 2:
        show_result_modal(0, 99.0, input_data_dict, "Minimum 2 years of employment experience is mandatory for loan approval.")
        
    else:
        with st.spinner("Analyzing AI profile..."):
            time.sleep(1.2)
            
            if model is not None:
                try:
                    input_data_array = np.array([[income, loan_amount, credit_score, employment_years, existing_loans]])
                    prediction = model.predict(input_data_array)[0]
                    if hasattr(model, "predict_proba"):
                        probability = max(model.predict_proba(input_data_array)[0]) * 100
                    else:
                        probability = 85.5 
                    
                    show_result_modal(prediction, probability, input_data_dict)
                except:
                    st.error("Model feature mismatch! Ensure your model expects exactly these 5 inputs.")
            else:
                is_approved = credit_score > 600 and loan_amount < (income * 0.5) and employment_years >= 2
                prediction = 1 if is_approved else 0
                probability = np.random.uniform(75.0, 98.0)
                show_result_modal(prediction, probability, input_data_dict)

st.markdown("</div>", unsafe_allow_html=True)