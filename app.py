import streamlit as st
import pandas as pd
import joblib
import time
import matplotlib.pyplot as plt

try:
    from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
    from reportlab.lib.styles import getSampleStyleSheet
    PDF_AVAILABLE = True
except:
    PDF_AVAILABLE = False

from retention_engine import generate_retention_strategies

# ----------------------------
# PAGE CONFIG
# ----------------------------
st.set_page_config(
    page_title="Customer Churn Intelligence",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ----------------------------
# PREMIUM UI CSS
# ----------------------------
st.markdown("""
<style>

/* Main spacing */
.block-container {
    padding-top: 2rem;
    padding-left: clamp(1rem, 4vw, 4rem);
    padding-right: clamp(1rem, 4vw, 4rem);
}

/* Gradient Header */
.premium-header {
    padding: 25px;
    border-radius: 18px;
    background: linear-gradient(135deg, #111827, #1f2937);
    color: white;
    text-align: center;
    margin-bottom: 30px;
}

/* Card style */
.premium-card {
    padding: 20px;
    border-radius: 16px;
    background-color: var(--secondary-background-color);
    box-shadow: 0 4px 12px rgba(0,0,0,0.08);
}

/* Buttons */
.stButton>button {
    width: 100%;
    height: 3em;
    border-radius: 10px;
    font-weight: 600;
    background: linear-gradient(135deg, #2563eb, #1e40af);
    color: white;
    border: none;
}

/* Risk badges */
.risk-high {
    background-color: #fee2e2;
    color: #b91c1c;
    padding: 8px 15px;
    border-radius: 20px;
    font-weight: 600;
    display: inline-block;
}
.risk-moderate {
    background-color: #fef3c7;
    color: #b45309;
    padding: 8px 15px;
    border-radius: 20px;
    font-weight: 600;
    display: inline-block;
}
.risk-low {
    background-color: #dcfce7;
    color: #166534;
    padding: 8px 15px;
    border-radius: 20px;
    font-weight: 600;
    display: inline-block;
}

/* Metric styling */
[data-testid="stMetric"] {
    background-color: var(--secondary-background-color);
    padding: 18px;
    border-radius: 15px;
    text-align: center;
}

/* Responsive Title */
h1 {
    font-size: clamp(24px, 4vw, 42px);
}

</style>
""", unsafe_allow_html=True)

# ----------------------------
# HEADER
# ----------------------------
st.markdown("""
<div class="premium-header">
    <h1>📊 Customer Churn Risk Intelligence</h1>
    <p>AI-powered prediction with strategic retention insights</p>
</div>
""", unsafe_allow_html=True)

# ----------------------------
# LOAD MODEL
# ----------------------------
try:
    model = joblib.load("model.pkl")
    le_gender = joblib.load("le_gender.pkl")
    le_geo = joblib.load("le_geo.pkl")
except Exception as e:
    st.error(f"Model loading failed: {e}")
    st.stop()

# ----------------------------
# SIDEBAR
# ----------------------------
with st.sidebar:
    st.header("Customer Profile")

    credit_score = st.slider("Credit Score", 300, 900, 600)
    geography = st.selectbox("Geography", le_geo.classes_)
    gender = st.selectbox("Gender", le_gender.classes_)
    age = st.slider("Age", 18, 90, 35)
    tenure = st.slider("Tenure", 0, 10, 3)
    balance = st.number_input("Balance", 0.0, 250000.0, 50000.0)
    num_products = st.slider("Products", 1, 4, 1)
    has_cr_card = st.selectbox("Credit Card", [0, 1])
    is_active = st.selectbox("Active Member", [0, 1])
    estimated_salary = st.number_input("Salary", 0.0, 200000.0, 50000.0)

# ----------------------------
# INPUT PREP
# ----------------------------
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

# ----------------------------
# ANALYZE BUTTON
# ----------------------------
if st.button("Analyze Customer Risk"):

    with st.spinner("Analyzing customer behavior patterns..."):
        time.sleep(1.5)

        probability = model.predict_proba(input_data)[0][1]
        prediction = model.predict(input_data)[0]

    if probability > 0.6:
        risk_level = "High Risk"
        risk_class = "risk-high"
    elif probability > 0.4:
        risk_level = "Moderate Risk"
        risk_class = "risk-moderate"
    else:
        risk_level = "Low Risk"
        risk_class = "risk-low"

    # ----------------------------
    # METRICS
    # ----------------------------
    col1, col2, col3 = st.columns(3)

    col1.metric("Churn Probability", f"{probability:.2%}")
    col2.markdown(f"<div class='{risk_class}'>{risk_level}</div>", unsafe_allow_html=True)
    col3.metric("Prediction", "Likely to Churn" if prediction == 1 else "Likely to Stay")

    st.divider()

    # ----------------------------
    # CHART
    # ----------------------------
    fig, ax = plt.subplots()
    ax.bar(["Stay", "Churn"], [1 - probability, probability])
    ax.set_ylim(0, 1)
    ax.set_ylabel("Probability")
    st.pyplot(fig, use_container_width=True)

    # ----------------------------
    # STRATEGIES
    # ----------------------------
    if probability > 0.6:
        st.subheader("Strategic Retention Recommendations")
        strategies = generate_retention_strategies(model, input_data)
        for s in strategies:
            st.write("•", s)

    # ----------------------------
    # PDF
    # ----------------------------
    if PDF_AVAILABLE:
        pdf_path = f"report_{int(time.time())}.pdf"
        doc = SimpleDocTemplate(pdf_path)
        styles = getSampleStyleSheet()
        elements = []

        elements.append(Paragraph("Customer Churn Risk Report", styles["Title"]))
        elements.append(Spacer(1, 12))
        elements.append(Paragraph(f"Churn Probability: {probability:.2%}", styles["Normal"]))
        elements.append(Paragraph(f"Risk Level: {risk_level}", styles["Normal"]))

        doc.build(elements)

        with open(pdf_path, "rb") as f:
            st.download_button(
                "📄 Download Full Risk Report",
                f,
                file_name="Churn_Risk_Report.pdf",
                use_container_width=True
            )
