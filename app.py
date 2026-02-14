import streamlit as st
import pandas as pd
import joblib
import os
import time
import matplotlib.pyplot as plt

# ---------------------------
# SAFE PDF IMPORT
# ---------------------------
try:
    from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
    from reportlab.lib.styles import getSampleStyleSheet
    PDF_AVAILABLE = True
except ImportError:
    PDF_AVAILABLE = False

from retention_engine import generate_retention_strategies

# ---------------------------
# PAGE CONFIG
# ---------------------------
st.set_page_config(
    page_title="Churn Risk Intelligence System",
    page_icon="📊",
    layout="wide"
)

# ---------------------------
# PREMIUM ENTERPRISE UI
# ---------------------------
st.markdown("""
<style>

.stApp {
    background: linear-gradient(135deg, #0f172a, #0b1120);
    color: white;
    font-family: 'Segoe UI', sans-serif;
}

h1 {
    background: linear-gradient(90deg, #3b82f6, #06b6d4);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    font-weight: 800;
}

.section-title {
    font-size: 22px;
    font-weight: 600;
    margin-top: 35px;
    margin-bottom: 15px;
    color: #e2e8f0;
}

.stButton>button {
    background: linear-gradient(90deg, #3b82f6, #06b6d4);
    color: white;
    border-radius: 12px;
    height: 3em;
    font-weight: 600;
    width: 100%;
    border: none;
    transition: 0.3s;
}

.stButton>button:hover {
    transform: scale(1.02);
    box-shadow: 0px 6px 20px rgba(59,130,246,0.4);
}

section[data-testid="stSidebar"] {
    background-color: #111827;
}

.stMetric {
    background: rgba(255,255,255,0.05);
    padding: 18px;
    border-radius: 14px;
}

.block-container {
    padding-top: 2rem;
}

</style>
""", unsafe_allow_html=True)

# ---------------------------
# TITLE
# ---------------------------
st.title("📊 Customer Churn Risk Intelligence Dashboard")
st.markdown("AI-powered churn prediction with strategic retention insights.")

# ---------------------------
# LOAD MODELS
# ---------------------------
try:
    model = joblib.load("model.pkl")
    le_gender = joblib.load("le_gender.pkl")
    le_geo = joblib.load("le_geo.pkl")
except Exception as e:
    st.error(f"❌ Model loading failed: {e}")
    st.stop()

# ---------------------------
# SIDEBAR INPUT
# ---------------------------
st.sidebar.header("Customer Profile")

credit_score = st.sidebar.slider("Credit Score", 300, 900, 600)
geography = st.sidebar.selectbox("Geography", le_geo.classes_)
gender = st.sidebar.selectbox("Gender", le_gender.classes_)
age = st.sidebar.slider("Age", 18, 90, 35)
tenure = st.sidebar.slider("Tenure (Years)", 0, 10, 3)
balance = st.sidebar.number_input("Balance", 0.0, 250000.0, 50000.0)
num_products = st.sidebar.slider("Number of Products", 1, 4, 1)
has_cr_card = st.sidebar.selectbox("Has Credit Card", [0, 1])
is_active = st.sidebar.selectbox("Active Member", [0, 1])
estimated_salary = st.sidebar.number_input("Estimated Salary", 0.0, 200000.0, 50000.0)

# ---------------------------
# PREPROCESS INPUT
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
# PREDICTION
# ---------------------------
if st.button("🚀 Analyze Customer Risk"):

    with st.spinner("Analyzing customer behavior patterns..."):
        time.sleep(1.5)

    probability = model.predict_proba(input_data)[0][1]
    prediction = model.predict(input_data)[0]

    if probability > 0.6:
        risk_level = "High Risk"
    elif probability > 0.4:
        risk_level = "Moderate Risk"
    else:
        risk_level = "Low Risk"

    # ---------------------------
    # KPI METRICS
    # ---------------------------
    st.markdown('<div class="section-title">📊 Risk Assessment Summary</div>', unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)

    col1.metric("Churn Probability", f"{probability:.2%}")

    if probability > 0.6:
        col2.metric("Risk Category", risk_level)
        st.error("🔴 High Risk Customer - Immediate Action Required")
    elif probability > 0.4:
        col2.metric("Risk Category", risk_level)
        st.warning("🟡 Moderate Risk - Monitor Closely")
    else:
        col2.metric("Risk Category", risk_level)
        st.success("🟢 Low Risk - Healthy Customer")

    col3.metric("Prediction", "Likely to Churn" if prediction == 1 else "Likely to Stay")

    # Progress bar
    st.progress(int(probability * 100))

    # ---------------------------
    # VISUALIZATION
    # ---------------------------
    st.markdown('<div class="section-title">📈 Risk Distribution</div>', unsafe_allow_html=True)

    fig, ax = plt.subplots()
    fig.patch.set_facecolor('#0f172a')
    ax.set_facecolor('#0f172a')

    ax.bar(
        ["Stay", "Churn"],
        [1 - probability, probability],
        color=["#22c55e", "#ef4444"]
    )

    ax.set_ylim(0, 1)
    ax.set_ylabel("Probability", color="white")
    ax.tick_params(colors='white')

    for i, value in enumerate([1 - probability, probability]):
        ax.text(i, value, f"{value:.1%}", ha='center', va='bottom', color="white")

    st.pyplot(fig)

    # ---------------------------
    # RETENTION STRATEGIES
    # ---------------------------
    if probability > 0.6:
        st.markdown('<div class="section-title">🎯 Strategic Retention Recommendations</div>', unsafe_allow_html=True)

        strategies = generate_retention_strategies(model, input_data)

        if strategies:
            for s in strategies:
                st.write("•", s)
        else:
            st.info("No strong retention action required.")

    # ---------------------------
    # PDF REPORT
    # ---------------------------
    if PDF_AVAILABLE:
        pdf_path = f"churn_report_{int(time.time())}.pdf"

        doc = SimpleDocTemplate(pdf_path)
        styles = getSampleStyleSheet()
        elements = []

        elements.append(Paragraph("Customer Churn Risk Report", styles["Title"]))
        elements.append(Spacer(1, 12))
        elements.append(Paragraph(f"Churn Probability: {probability:.2%}", styles["Normal"]))
        elements.append(Paragraph(f"Risk Category: {risk_level}", styles["Normal"]))
        elements.append(Spacer(1, 12))

        doc.build(elements)

        with open(pdf_path, "rb") as f:
            st.download_button(
                "📄 Download Risk Report (PDF)",
                f,
                file_name="Churn_Risk_Report.pdf"
            )
