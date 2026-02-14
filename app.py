import streamlit as st
import pandas as pd
import joblib
import os
import time
import matplotlib.pyplot as plt

# Try importing reportlab safely
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
# PROFESSIONAL STYLE
# ---------------------------
st.markdown("""
<style>
body {
    background-color: #f4f6f9;
}
.section-title {
    font-size: 22px;
    font-weight: 600;
    margin-top: 25px;
}
.stButton>button {
    background-color: #111827;
    color: white;
    border-radius: 6px;
    height: 3em;
    font-weight: 500;
}
</style>
""", unsafe_allow_html=True)

st.title("📊 Customer Churn Risk Intelligence Dashboard")
st.markdown("AI-powered churn prediction with strategic retention insights.")

# ---------------------------
# PATH SETUP
# ---------------------------
import os
import joblib

BASE_DIR = os.path.dirname(__file__)

model = joblib.load(os.path.join(BASE_DIR, "model.pkl"))
le_gender = joblib.load(os.path.join(BASE_DIR, "le_gender.pkl"))
le_geo = joblib.load(os.path.join(BASE_DIR, "le_geo.pkl"))


# ---------------------------
# LOAD MODEL SAFELY
# ---------------------------
try:
    model = joblib.load(os.path.join(MODEL_DIR, "model.pkl"))
    le_gender = joblib.load(os.path.join(MODEL_DIR, "le_gender.pkl"))
    le_geo = joblib.load(os.path.join(MODEL_DIR, "le_geo.pkl"))
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
if st.button("Analyze Customer Risk"):

    probability = model.predict_proba(input_data)[0][1]
    prediction = model.predict(input_data)[0]

    # Risk category logic
    if probability > 0.6:
        risk_level = "High Risk"
    elif probability > 0.4:
        risk_level = "Moderate Risk"
    else:
        risk_level = "Low Risk"

    # ---------------------------
    # KPI METRICS
    # ---------------------------
    st.markdown('<div class="section-title">Risk Assessment Summary</div>', unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)

    col1.metric("Churn Probability", f"{probability:.2%}")
    col2.metric("Risk Category", risk_level)
    col3.metric("Prediction", "Likely to Churn" if prediction == 1 else "Likely to Stay")

    # ---------------------------
    # VISUALIZATION
    # ---------------------------
    st.markdown('<div class="section-title">Risk Distribution</div>', unsafe_allow_html=True)

    fig, ax = plt.subplots()
    ax.bar(["Stay", "Churn"], [1 - probability, probability])
    ax.set_ylim(0, 1)
    ax.set_ylabel("Probability")

    for i, value in enumerate([1 - probability, probability]):
        ax.text(i, value, f"{value:.1%}", ha='center', va='bottom')

    st.pyplot(fig)

    # ---------------------------
    # RETENTION STRATEGIES
    # ---------------------------
    strategies = []

    if probability > 0.6:
        st.markdown('<div class="section-title">Strategic Retention Recommendations</div>', unsafe_allow_html=True)

        strategies = generate_retention_strategies(model, input_data)

        if strategies:
            for s in strategies:
                st.write("•", s)
        else:
            st.info("No strong retention action required.")

    # ---------------------------
    # PDF REPORT (Only if available)
    # ---------------------------
    if PDF_AVAILABLE:
        pdf_path = os.path.join(BASE_DIR, f"churn_report_{int(time.time())}.pdf")
        doc = SimpleDocTemplate(pdf_path)
        elements = []
        styles = getSampleStyleSheet()

        elements.append(Paragraph("Customer Churn Risk Report", styles['Title']))
        elements.append(Spacer(1, 12))
        elements.append(Paragraph(f"Churn Probability: {probability:.2%}", styles['Normal']))
        elements.append(Spacer(1, 12))
        elements.append(Paragraph(f"Risk Category: {risk_level}", styles['Normal']))
        elements.append(Spacer(1, 12))

        if strategies:
            elements.append(Paragraph("Recommended Retention Actions:", styles['Heading2']))
            elements.append(Spacer(1, 8))
            for s in strategies:
                elements.append(Paragraph(f"- {s}", styles['Normal']))
                elements.append(Spacer(1, 6))

        doc.build(elements)

        with open(pdf_path, "rb") as f:
            st.download_button("Download Risk Report (PDF)", f, file_name="Churn_Risk_Report.pdf")
    else:
        st.warning("PDF feature unavailable (install reportlab to enable).")

