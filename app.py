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
# PAGE CONFIG
# ---------------------------
st.set_page_config(
    page_title="Churn Risk Intelligence System",
    page_icon="📊",
    layout="wide"
)

# ---------------------------
# PREMIUM UI
# ---------------------------
st.markdown("""
<style>

.stApp {
    background: linear-gradient(135deg, #0f172a, #0b1120);
    color: white;
    font-family: 'Segoe UI', sans-serif;
}

h1 {
    text-align: center;
    background: linear-gradient(90deg, #3b82f6, #06b6d4);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

.card {
    background: rgba(255,255,255,0.05);
    padding: 25px;
    border-radius: 18px;
    margin-bottom: 20px;
}

.stButton>button {
    background: linear-gradient(90deg, #3b82f6, #06b6d4);
    color: white;
    border-radius: 12px;
    height: 3em;
    font-weight: 600;
    width: 100%;
    border: none;
}

</style>
""", unsafe_allow_html=True)

# ---------------------------
# TITLE
# ---------------------------
st.title("📊 Customer Churn Risk Intelligence Dashboard")
st.markdown("<center>AI-powered churn prediction with strategic retention insights</center>", unsafe_allow_html=True)

# ---------------------------
# LOAD MODELS
# ---------------------------
try:
    model = joblib.load("model.pkl")
    le_gender = joblib.load("le_gender.pkl")
    le_geo = joblib.load("le_geo.pkl")
except Exception as e:
    st.error(f"Model loading failed: {e}")
    st.stop()

# ---------------------------
# INPUT SECTION (FRONT)
# ---------------------------
st.markdown("## 🧾 Customer Information")

col1, col2, col3 = st.columns(3)

with col1:
    credit_score = st.slider("Credit Score", 300, 900, 600)
    geography = st.selectbox("Geography", le_geo.classes_)
    gender = st.selectbox("Gender", le_gender.classes_)

with col2:
    age = st.slider("Age", 18, 90, 35)
    tenure = st.slider("Tenure (Years)", 0, 10, 3)
    balance = st.number_input("Balance", 0.0, 250000.0, 50000.0)

with col3:
    num_products = st.slider("Number of Products", 1, 4, 1)
    has_cr_card = st.selectbox("Has Credit Card", [0, 1])
    is_active = st.selectbox("Active Member", [0, 1])
    estimated_salary = st.number_input("Estimated Salary", 0.0, 200000.0, 50000.0)

st.markdown("---")

# ---------------------------
# ANALYZE BUTTON (CENTER)
# ---------------------------
center_col = st.columns([1,2,1])[1]

with center_col:
    analyze = st.button("🚀 Analyze Customer Risk")

# ---------------------------
# PREDICTION
# ---------------------------
if analyze:

    with st.spinner("Analyzing behavior patterns..."):
        time.sleep(1.2)

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

    probability = model.predict_proba(input_data)[0][1]
    prediction = model.predict(input_data)[0]

    if probability > 0.6:
        risk_level = "High Risk"
        risk_color = "🔴"
    elif probability > 0.4:
        risk_level = "Moderate Risk"
        risk_color = "🟡"
    else:
        risk_level = "Low Risk"
        risk_color = "🟢"

    # ---------------------------
    # RESULTS SECTION
    # ---------------------------
    st.markdown("## 📊 Risk Assessment Results")

    m1, m2, m3 = st.columns(3)
    m1.metric("Churn Probability", f"{probability:.2%}")
    m2.metric("Risk Level", f"{risk_color} {risk_level}")
    m3.metric("Prediction", "Likely to Churn" if prediction == 1 else "Likely to Stay")

    st.progress(int(probability * 100))

    # ---------------------------
    # CHART
    # ---------------------------
    fig, ax = plt.subplots()
    fig.patch.set_facecolor('#0f172a')
    ax.set_facecolor('#0f172a')

    ax.bar(["Stay", "Churn"], [1 - probability, probability],
           color=["#22c55e", "#ef4444"])

    ax.set_ylim(0, 1)
    ax.tick_params(colors='white')
    ax.set_ylabel("Probability", color="white")

    st.pyplot(fig)

    # ---------------------------
    # RETENTION STRATEGIES
    # ---------------------------
    if probability > 0.6:
        st.markdown("## 🎯 Retention Strategies")
        strategies = generate_retention_strategies(model, input_data)
        if strategies:
            for s in strategies:
                st.write("•", s)

    # ---------------------------
    # PDF DOWNLOAD
    # ---------------------------
    if PDF_AVAILABLE:
        pdf_path = f"churn_report_{int(time.time())}.pdf"
        doc = SimpleDocTemplate(pdf_path)
        styles = getSampleStyleSheet()
        elements = []

        elements.append(Paragraph("Customer Churn Risk Report", styles["Title"]))
        elements.append(Spacer(1, 12))
        elements.append(Paragraph(f"Churn Probability: {probability:.2%}", styles["Normal"]))
        elements.append(Paragraph(f"Risk Level: {risk_level}", styles["Normal"]))

        doc.build(elements)

        with open(pdf_path, "rb") as f:
            st.download_button("📄 Download PDF Report", f, file_name="Churn_Report.pdf")
