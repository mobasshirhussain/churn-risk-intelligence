import streamlit as st

st.set_page_config(page_title="Customer Churn Intelligence", layout="wide")

# ===================== PREMIUM CSS =====================

st.markdown("""
<style>

/* Background */
.stApp {
    background: linear-gradient(135deg, #0f172a, #0b1120);
    font-family: 'Segoe UI', sans-serif;
}

/* ===== TITLE ===== */
.main-title {
    text-align: center;
    font-size: clamp(30px, 5vw, 48px);
    font-weight: 800;
    background: linear-gradient(90deg, #3b82f6, #06b6d4);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin-bottom: 10px;
}

.sub-title {
    text-align: center;
    font-size: 18px;
    color: #cbd5e1;
    margin-bottom: 40px;
}

/* ===== GLASS CARD ===== */
.block-container {
    padding-top: 2rem;
}

section.main > div {
    background: rgba(255, 255, 255, 0.05);
    padding: 30px;
    border-radius: 20px;
    backdrop-filter: blur(12px);
    box-shadow: 0px 0px 40px rgba(0,0,0,0.4);
}

/* ===== INPUT FIELDS ===== */
.stSlider > div {
    color: #ffffff;
}

.stSelectbox > div {
    background-color: #1e293b !important;
    border-radius: 10px;
}

/* ===== BUTTON ===== */
.stButton > button {
    width: 100%;
    border-radius: 12px;
    background: linear-gradient(90deg, #3b82f6, #06b6d4);
    color: white;
    font-weight: 600;
    padding: 12px;
    border: none;
    transition: 0.3s;
}

.stButton > button:hover {
    transform: scale(1.02);
    box-shadow: 0px 5px 20px rgba(59,130,246,0.5);
}

/* ===== RISK BADGE ===== */
.low-risk {
    background-color: #064e3b;
    color: #34d399;
    padding: 12px;
    border-radius: 10px;
    text-align: center;
    font-weight: 600;
}

.medium-risk {
    background-color: #78350f;
    color: #facc15;
    padding: 12px;
    border-radius: 10px;
    text-align: center;
    font-weight: 600;
}

.high-risk {
    background-color: #7f1d1d;
    color: #f87171;
    padding: 12px;
    border-radius: 10px;
    text-align: center;
    font-weight: 600;
}

</style>
""", unsafe_allow_html=True)

# ===================== HEADER =====================

st.markdown('<div class="main-title">📊 Customer Churn Intelligence</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-title">AI-powered Customer Risk Prediction System</div>', unsafe_allow_html=True)

# ===================== INPUT SECTION =====================

st.subheader("📋 Enter Customer Details")

credit_score = st.slider("Credit Score", 300, 900, 600)
geography = st.selectbox("Geography", ["France", "Germany", "Spain"])
gender = st.selectbox("Gender", ["Male", "Female"])
age = st.slider("Age", 18, 80, 35)
tenure = st.slider("Tenure (Years)", 0, 10, 3)

# ===================== PREDICT BUTTON =====================

if st.button("🔍 Predict Churn Risk"):

    with st.spinner("Analyzing customer data..."):
        import time
        time.sleep(2)

    # Dummy risk logic
    if credit_score > 700:
        st.markdown('<div class="low-risk">🟢 Low Churn Risk</div>', unsafe_allow_html=True)
    elif credit_score > 500:
        st.markdown('<div class="medium-risk">🟡 Medium Churn Risk</div>', unsafe_allow_html=True)
    else:
        st.markdown('<div class="high-risk">🔴 High Churn Risk</div>', unsafe_allow_html=True)
