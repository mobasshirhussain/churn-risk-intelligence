import streamlit as st
import pandas as pd
import joblib
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
# PAGE CONFIG (MOBILE OPTIMIZED)
# ---------------------------
st.set_page_config(
    page_title="Customer Churn Risk Intelligence",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ---------------------------
# CLEAN RESPONSIVE CSS
# ---------------------------
st.markdown("""
<style>

/* Main container padding responsive */
.block-container {
    padding-top: 2rem;
    padding-bottom: 2rem;
    padding-left: clamp(1rem, 4vw, 4rem);
    padding-right: clamp(1rem, 4vw, 4rem);
}

/* Title responsive */
h1 {
    font-size: clamp(24px, 4vw, 42px);
}

/* Section headings */
.section-title {
    font-size: clamp(18px, 2vw, 24px);
    font-weight: 600;
    margin-top: 25px;
    margin-bottom: 10px;
}

/* Button full width */
.stButton > button {
    width: 100%;
    height: 3em;
    border-radius: 8px;
    background-color: #111827;
    color: white;
    font-weight: 500;
}

/* Metric spacing */
[data-testid="stMetric"] {
    background-color: #f9fafb;
    padding: 15px;
    border-radius: 10px;
    text-align: center;
}

/* Make chart responsive */
canvas {
    max-width: 100% !important;
}

/* Reduce extra spacing on mobile */
@media (max-width: 768px) {
    .block-container {
        padding-left: 1rem;
        padding-right: 1rem;
    }
}

</style>
""", unsafe_allow_html=True)

# ---------------------------
# HEADER
# ---------------------------
st.title("📊 Customer Churn Risk Intelligence Dashboard")
st.markdown("AI-powered churn prediction with strategic retention insights.")

st.divider()

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
with st.sidebar:
    st.header("Customer Profile")

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

    if probability > 0.6:
        risk_level = "High Risk"
    elif probability > 0.4:
        risk_level = "Moderate Risk"
    else:
        risk_level = "Low Risk"

    # ---------------------------
    # METRICS
    # ---------------------------
    st.markdown('<div class="section-title">Risk Assessment Summary</div>', unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)

    col1.metric("Churn Probability", f"{probability:.2%}")
    col2.metric("Risk Category", risk_level)
    col3.metric("Prediction", "Likely to Churn" if prediction == 1 else "Likely to Stay")

    # ---------------------------
    # CHART
    # ---------------------------
    st.markdown('<div class="section-title">Risk Distribution</div>', unsafe_allow_html=True)

    fig, ax = plt.subplots()
    ax.bar(["Stay", "Churn"], [1 - probability, probability])
    ax.set_ylim(0, 1)
    ax.set_ylabel("Probability")

    for i, value in enumerate([1 - probability, probability]):
        ax.text(i, value, f"{value:.1%}", ha='center', va='bottom')

    st.pyplot(fig, use_container_width=True)

    # ---------------------------
    # RETENTION STRATEGIES
    # ---------------------------
    if probability > 0.6:
        st.markdown('<div class="section-title">Strategic Retention Recommendations</div>', unsafe_allow_html=True)

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
                file_name="Churn_Risk_Report.pdf",
                use_container_width=True
            )
    else:
        st.warning("PDF feature unavailable (reportlab not installed).")
