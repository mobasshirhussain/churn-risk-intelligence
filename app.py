import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import time

st.set_page_config(page_title="Customer Churn Intelligence", layout="wide")

# ===================== PREMIUM CSS =====================
st.markdown("""
<style>
.stApp {
    background: linear-gradient(135deg, #0f172a, #0b1120);
    font-family: 'Segoe UI', sans-serif;
}

.main-title {
    text-align: center;
    font-size: clamp(30px, 5vw, 48px);
    font-weight: 800;
    background: linear-gradient(90deg, #3b82f6, #06b6d4);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

.sub-title {
    text-align: center;
    font-size: 18px;
    color: #cbd5e1;
    margin-bottom: 40px;
}

section.main > div {
    background: rgba(255, 255, 255, 0.05);
    padding: 30px;
    border-radius: 20px;
    backdrop-filter: blur(12px);
    box-shadow: 0px 0px 40px rgba(0,0,0,0.4);
}

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
</style>
""", unsafe_allow_html=True)

# ===================== HEADER =====================
st.markdown('<div class="main-title">📊 Customer Churn Intelligence</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-title">AI-powered Customer Risk Prediction System</div>', unsafe_allow_html=True)

# ===================== INPUT =====================
st.subheader("📋 Enter Customer Details")

credit_score = st.slider("Credit Score", 300, 900, 600)
geography = st.selectbox("Geography", ["France", "Germany", "Spain"])
gender = st.selectbox("Gender", ["Male", "Female"])
age = st.slider("Age", 18, 80, 35)
tenure = st.slider("Tenure (Years)", 0, 10, 3)

# ===================== PREDICT =====================
if st.button("🔍 Predict Churn Risk"):

    with st.spinner("Analyzing customer data..."):
        time.sleep(2)

    # 🔥 Replace this with your real model
    probability = np.clip((700 - credit_score) / 700 + age/200, 0, 1)

    churn_percent = round(probability * 100, 2)

    st.subheader("📊 Prediction Result")

    # Risk Category
    if churn_percent < 40:
        st.success(f"🟢 Low Risk ({churn_percent}%)")
    elif churn_percent < 70:
        st.warning(f"🟡 Medium Risk ({churn_percent}%)")
    else:
        st.error(f"🔴 High Risk ({churn_percent}%)")

    # Progress Bar
    st.progress(int(churn_percent))

    # ===================== PLOT =====================
    st.subheader("📈 Churn Probability Chart")

    labels = ["Stay", "Churn"]
    values = [100 - churn_percent, churn_percent]

    fig, ax = plt.subplots()
    ax.bar(labels, values)
    ax.set_ylabel("Probability (%)")
    ax.set_ylim(0,100)

    st.pyplot(fig)
