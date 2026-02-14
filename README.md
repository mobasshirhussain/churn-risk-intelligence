# 📊 Churn Risk Intelligence

AI-powered customer churn prediction dashboard with intelligent retention strategy insights.

---

## 🚀 Overview

Customer retention is one of the most critical challenges faced by modern businesses. Acquiring new customers is significantly more expensive than retaining existing ones. This project presents a Machine Learning-based system that predicts customer churn risk and provides intelligent retention recommendations.

The system is deployed using an interactive Streamlit dashboard for real-time analysis.

---

## 🎯 Project Objectives

- Build a machine learning model to predict customer churn  
- Deploy the model using a user-friendly web dashboard  
- Design a retention engine to simulate churn reduction strategies  
- Generate automated PDF reports summarizing prediction results  

---

## 📂 Dataset Description

The dataset includes the following customer attributes:

- Credit Score  
- Geography  
- Gender  
- Age  
- Tenure  
- Balance  
- Number of Products  
- Has Credit Card  
- Is Active Member  
- Estimated Salary  

**Target Variable:**  
- `Churn` – Indicates whether the customer has left the company.

---

## 🔧 Data Preprocessing

The following preprocessing steps were performed:

- Handling missing values  
- Label encoding categorical features  
- Feature selection  
- Train-test split  

These steps ensured clean and model-ready data.

---

## 🤖 Model Development

A supervised classification model was trained to predict customer churn.

The trained model:

- Accepts customer input data  
- Predicts churn (Yes/No)  
- Provides churn probability score  

The model was saved using `joblib` for deployment.

---

## 💻 System Implementation

The application is deployed using **Streamlit**, providing a clean and professional dashboard interface.

Users can:

- Enter customer details  
- Analyze churn risk  
- View probability score  
- See risk category (Low / Moderate / High)  
- Visualize risk distribution  
- Download a PDF report  

---

## 🧠 Retention Logic Engine

When churn probability exceeds a defined threshold:

- Customer attributes are analyzed  
- Behavioral improvements are simulated  
- Impact on churn probability is evaluated  
- Strategic retention recommendations are generated  

This adds practical business value to the system.

---

## 📄 Automated Report Generation

The system generates a downloadable PDF report containing:

- Churn probability  
- Risk category  
- Prediction result  
- Recommended retention strategies  

---

## 📊 Key Insights

Customers with the following characteristics are more likely to churn:

- Low engagement  
- Low tenure  
- Inactive membership  
- Fewer product holdings  

---

## 🏆 Project Strengths

- Machine learning-based predictive analytics  
- Clean and professional dashboard interface  
- Intelligent retention simulation  
- Automated PDF report generation  
- Deployment-ready architecture  

---

## 🛠️ Tech Stack

- Python  
- Scikit-learn  
- Pandas  
- NumPy  
- Streamlit  
- Matplotlib  
- ReportLab  

---

## ▶️ How to Run Locally

1. Clone the repository  
2. Install dependencies:

```
pip install -r requirements.txt
```

3. Run the application:

```
streamlit run app.py
```

---

## 📌 Conclusion

This project demonstrates how machine learning can enhance customer retention strategies. By combining predictive analytics with retention simulation, the system provides actionable business insights to reduce churn and improve long-term profitability.
