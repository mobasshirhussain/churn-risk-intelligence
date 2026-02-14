import streamlit as st
import pandas as pd
import joblib
import time
import matplotlib.pyplot as plt

# ---------------------------
# PAGE CONFIG (CENTERED LIKE MEDICAL UI)
# ---------------------------
st.set_page_config(
    page_title="Customer Risk Analyzer",
    page_icon="📊",
    layout="centered"
)

# ---------------------------
# CLEAN MEDICAL-STYLE CSS
# ---------------------------
st.markdown("""
<style>

/* Center container */
.block-container {
    padding-top: 3rem;
    padding-bottom: 3rem;
    max-width: 750px;
}

/* Main Title */
.main-title {
    text-align: center;
    font-size: clamp(28px, 5vw, 46px);
    font-weight: 700;
    color: #1f2937;
}

/* Subtitle */
.sub-title {
    text-align: center;
    font-size: 18px;
    color: #6b7280;
    margin-bottom: 40px;
}

/* Section title */
.section-title {
    font-size: 22px;
    font-weight: 600;
    margin-top: 25px;
}

/* Button style */
.stButton > button {
    width: 100%;
    height: 3.2em;
    border-radius: 12px;
    font-size: 18px;
    font-weight: 600;
    background-color: #111827;
    color: white;
    border: none;
}

/* Selectbox & inputs rounded */
div[data-baseweb="select"] > div,
input {
    border-radius: 12px !important;
}

/* Metric card style */
[data-testid="stMetric"] {
    background-color: #f3f4f6;
    padding: 15px;
    border-radius: 12px;
    text-align: center;
}

/* Mobile padding */
@media (max-width: 768px) {
    .block-container {
        padding-left: 1rem;
        padding-right: 1rem;
    }
}

</style>
""", unsafe_allow_html=True)

# ---------------------------
# HEADER SECTION
# ---------------------------
st.markdown('<div class="main-title">📊 Customer Churn Intelligence</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-title">AI-powered Customer Risk Prediction System</div>', unsafe_allow_html=True)

st.markdown("### 🧾 Enter Customer Details")

# ---------------------------
# LOAD MODEL
# ---------------------------
try:
    model = joblib.load("model.pkl")
    le_gender = joblib.load("le_gender.pkl")
    le_geo = joblib.load("le_geo.pkl")
except Exception as e:
    st.error(f"Model loading failed: {e}")
    st.stop()

# ---------------------------
# INPUT SECTION (FRONT PAGE)
# ---------------------------
credit_score = st.slider("Credit Score", 300, 900, 600)
geography = st.selectbox("Geography", le_geo.classes_)
gender = st.selectbox("Gender", le_gender.classes_)
age = st.slider("Age", 18, 90, 35)
tenure = st.slider("Tenure (Years)", 0, 10, 3)
balance = st.number_input("Balance", 0.0, 250000.0, 50000.0)
num_products = st.slider("Number of Products", 1, 4, 1)
has_cr_card = st.selectbox("Has Credit Card", [0, 1])
is_active = st.selectbox("Active Member", [0, 1])
estimated_salary = st.number_input("Estimated Salary", 0.0, 200000.0, 50000.0)

# ---------------------------
# PREP INPUT
# ---------------------------
geo_encoded = le_geo.transform([geography])[0]
gender_encoded = le_gender.transform([gender])[0]

input_data = pd.DataFrame([{
    "CreditScore": credit_score,
    "Geography": geo_encoded,
    "Gender": gender_encoded,
    "Age": age,
    "Tenure": tenure,
    "Balance": balance,
    "NumOfProducts": num_products,
    "HasCrCard": has_cr_card,
    "IsActiveMember": is_active,
    "EstimatedSalary": estimated_salary
}])

if hasattr(model, "feature_names_in_"):
    input_data = input_data[model.feature_names_in_]

# ---------------------------
# PREDICT BUTTON (BIG LIKE MEDICAL APP)
# ---------------------------
if st.button("🚀 Analyze Customer Risk"):

    with st.spinner("Analyzing customer behavior..."):
        time.sleep(1.2)

        probability = model.predict_proba(input_data)[0][1]
        prediction = model.predict(input_data)[0]

    if probability > 0.6:
        risk_level = "High Risk 🔴"
    elif probability > 0.4:
        risk_level = "Moderate Risk 🟡"
    else:
        risk_level = "Low Risk 🟢"

    st.markdown("### 📊 Risk Assessment Summary")

    col1, col2 = st.columns(2)

    col1.metric("Churn Probability", f"{probability:.2%}")
    col2.metric("Risk Level", risk_level)

    st.markdown("### 📈 Risk Distribution")

    fig, ax = plt.subplots()
    ax.bar(["Stay", "Churn"], [1 - probability, probability])
    ax.set_ylim(0, 1)
    st.pyplot(fig, use_container_width=True)

    if probability > 0.6:
        st.markdown("### 💡 Recommended Retention Actions")
        strategies = generate_retention_strategies(model, input_data)
        for s in strategies:
            st.write("•", s)
