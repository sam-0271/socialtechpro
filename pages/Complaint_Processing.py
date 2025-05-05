import streamlit as st
import pandas as pd
import joblib
from datetime import datetime, timedelta
import spacy
import os

# ===========================
# Load Models and Encoders
# ===========================
MODEL_DIR = "models"

priority_model = joblib.load(os.path.join(MODEL_DIR, "newpriority_predictor.pkl"))
resolution_model = joblib.load(os.path.join(MODEL_DIR, "resolution_time_predictorr.pkl"))

le_area = joblib.load(os.path.join(MODEL_DIR, "labelencoder_area.pkl"))
le_type = joblib.load(os.path.join(MODEL_DIR, "labelencoder_type.pkl"))
le_priority_output = joblib.load(os.path.join(MODEL_DIR, "newpriority_label_encoder.pkl"))

scaler = joblib.load(os.path.join(MODEL_DIR, "scalerr.pkl"))
X_columns = joblib.load(os.path.join(MODEL_DIR, "x_columns.pkl"))

nlp = spacy.load("en_core_web_sm")

# ===========================
# Department Mapping
# ===========================
type_to_department = {
    "Garbage Issue": "Municipal Waste Management Department",
    "Electricity Issue": "Electricity Distribution Department",
    "Illegal Parking": "Traffic and Transportation Department",
    "Tree Falling": "Urban Forestry and Landscaping Department",
    "Road Damage": "Public Works Department",
    "Animal Nuisance": "Animal Control and Welfare Department",
    "Streetlight Issue": "Urban Lighting and Infrastructure Department",
    "Noise Pollution": "Environmental Protection Department",
    "Water Issue": "Water Supply and Sanitation Department",
    "Sewage Problem": "Sewerage and Drainage Department"
}

# ===========================
# UI Styling & Layout
# ===========================
st.set_page_config(page_title="Smart Complaint Management System", page_icon="📣", layout="wide")

# Custom CSS to enhance the page styling
st.markdown("""
    <style>
        .big-font {
            font-size: 24px !important;
            font-weight: bold;
            color: #ff6347;
        }
        .header-font {
            font-size: 28px !important;
            color: #008080;
        }
        .section-header {
            font-size: 22px !important;
            color: #4169e1;
        }
        .card {
            background-color: #f0f8ff;
            padding: 20px;
            border-radius: 10px;
            margin-top: 20px;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
        }
    </style>
""", unsafe_allow_html=True)

# Title
st.title("📣 **Smart Complaint Management System**")
st.markdown("### **Submit Your Complaint and Predict Resolution Time**")
st.markdown("---")

# Step 1: Complaint Filing
st.header("📝 **Step 1: File a Complaint**")
st.markdown("---")

with st.form("complaint_form"):
    complaint_text = st.text_area("• Complaint Description", "Uncollected garbage near XYZ lane in Hadapsar, causing health hazard.")
    area = st.selectbox("• Area", le_area.classes_)
    problem_type = st.selectbox("• Problem Type", le_type.classes_)
    filing_date = st.date_input("• Filing Date", datetime.today())
    submitted = st.form_submit_button("Submit Complaint")

if submitted:
    st.session_state['complaint_text'] = complaint_text
    st.session_state['area'] = area
    st.session_state['problem_type'] = problem_type
    st.session_state['filing_date'] = filing_date

    department = type_to_department.get(problem_type, "General Complaints Department")

    input_df = pd.DataFrame([{
        "complaint_text": complaint_text,
        "type": problem_type,
        "area": area,
        "type_emphasis": problem_type
    }]).fillna('missing').astype(str)

    priority_encoded = priority_model.predict(input_df)[0]
    priority = le_priority_output.inverse_transform([priority_encoded])[0]

    st.session_state['department'] = department
    st.session_state['priority'] = priority

    st.subheader("📍 **Step 2: Classification Results**")
    st.write(f"• 🏢 **Assigned Department**: {department}")
    st.write(f"• 🔺 **Predicted Priority**: {priority}")

    st.markdown("---")
    st.markdown("<h4 class='big-font'>Your complaint has been successfully filed! 🎉</h4>", unsafe_allow_html=True)

# Step 3: ETA Prediction
if 'department' in st.session_state and st.button("▶️ **Predict Estimated Resolution Time (ETA)**"):
    st.subheader("⏳ **Step 3: Predicted Resolution Time**")
    st.markdown("---")

    eta_input = pd.DataFrame([{
        "area": st.session_state['area'],
        "problem_type": st.session_state['problem_type'],
        "department": st.session_state['department'],
        "filing_year": st.session_state['filing_date'].year,
        "filing_month": st.session_state['filing_date'].month,
        "filing_day": st.session_state['filing_date'].day
    }])

    eta_input = pd.get_dummies(eta_input)
    eta_input = eta_input.reindex(columns=X_columns, fill_value=0).astype(float)
    eta_scaled = scaler.transform(eta_input)

    predicted_days = resolution_model.predict(eta_scaled)[0]
    expected_completion = st.session_state['filing_date'] + timedelta(days=predicted_days)

    st.write(f"📅 **Predicted Resolution Time**: {predicted_days:.1f} days")
    st.write(f"✅ **Expected Completion Date**: {expected_completion.strftime('%d %B %Y')}")

    st.success("🎉 **Complaint processed successfully!**")
    st.info("💰 **Check Budget Allocation: Go to Budget_Analysis.py**")

    # Add Call-to-Action Button
    st.markdown("""
    <div style='text-align:center;'>
        <a href="https://your-link-here.com" target="_blank">
            <button style="background-color:#008080; color:white; padding:10px 20px; border-radius:5px; font-size:16px;">
                Visit Budget Analysis
            </button>
        </a>
    </div>
    """, unsafe_allow_html=True)
