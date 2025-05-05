# Budget_Analysis.py

import streamlit as st
import pandas as pd
import joblib
import os
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick

# Load Models & Encoders
MODEL_DIR = "models"

try:
    total_budget_model = joblib.load(os.path.join(MODEL_DIR, "total_budget_model.pkl"))
    used_budget_model = joblib.load(os.path.join(MODEL_DIR, "used_budget_model.pkl"))
    budget_label_encoder_dept = joblib.load(os.path.join(MODEL_DIR, "budget_label_encoder_dept.pkl"))
    budget_label_encoder_area = joblib.load(os.path.join(MODEL_DIR, "budget_label_encoder_area.pkl"))
except Exception as e:
    st.error(f"❌ Model loading failed: {e}")
    st.stop()

# UI Setup
st.set_page_config(page_title="Budget Analysis", page_icon="💸", layout="wide")
st.title("💸 Department Budget Analysis & Visualization")

if 'department' not in st.session_state:
    st.warning("⚠️ Please first file a complaint using *Complaint_Management.py*")
else:
    st.subheader("💰 Step 4: Budget Prediction & Charts")

    # Inputs
    selected_area = st.selectbox("• Select Area", budget_label_encoder_area.classes_,
                                 index=list(budget_label_encoder_area.classes_).index(st.session_state['area']))
    department = st.session_state['department']

    actual_total_budget = st.number_input("• Actual Total Budget (₹)", min_value=0, value=1000000, step=10000)
    actual_used_budget = st.number_input("• Actual Used Budget (₹)", min_value=0, value=400000, step=10000)
    actual_remaining_budget = st.number_input("• Actual Remaining Budget (₹)", min_value=0, value=200000, step=10000)

    if st.button("🧾 Predict Budget & Show Visuals", key="predict_compare_budget"):
        try:
            # Encode inputs
            dept_encoded = budget_label_encoder_dept.transform([department])[0]
            area_encoded = budget_label_encoder_area.transform([selected_area])[0]

            # Predict Total Budget
            total_input = pd.DataFrame([{
                "used_budget": actual_used_budget,
                "remaining_budget": actual_remaining_budget,
                "department_encoded": dept_encoded,
                "area_encoded": area_encoded
            }])
            predicted_total = total_budget_model.predict(total_input)[0]

            # Predict Used Budget
            used_input = pd.DataFrame([{
                "total_budget": predicted_total,
                "remaining_budget": actual_remaining_budget,
                "department_encoded": dept_encoded,
                "area_encoded": area_encoded
            }])
            predicted_used = used_budget_model.predict(used_input)[0]
            predicted_remaining = predicted_total - predicted_used

            # Check for potential corruption if the difference is large
            corruption_threshold = 0.2  # 20% difference considered as corruption
            corruption_message = ""

            total_budget_diff = abs(actual_total_budget - predicted_total) / actual_total_budget
            used_budget_diff = abs(actual_used_budget - predicted_used) / actual_used_budget

            if total_budget_diff > corruption_threshold or used_budget_diff > corruption_threshold:
                corruption_message = "⚠️ Potential Corruption Detected: Large budget discrepancy!"

            # Show Prediction
            st.success("✅ Budget Prediction Completed")
            st.metric("Predicted Total Budget", f"₹{predicted_total:,.2f}")
            st.metric("Predicted Used Budget", f"₹{predicted_used:,.2f}")
            st.metric("Predicted Remaining Budget", f"₹{predicted_remaining:,.2f}")

            # Show corruption warning if applicable
            if corruption_message:
                st.warning(corruption_message)

            # === 📊 Charts Section ===
            st.header("📊 Visual Comparisons")

            # 1️⃣ Bar Chart (Side-by-Side)
            st.subheader("📊 Bar Chart: Actual vs Predicted")
            view_mode = st.radio("View Mode", ["Absolute (₹)", "Percentage (%)"])

            def format_inr(value):
                if value >= 1e6:
                    return f'₹{value/1e6:.1f}M'
                elif value >= 1e3:
                    return f'₹{value/1e3:.1f}K'
                return f'₹{value:.0f}'

            # Data for Chart
            if view_mode == "Absolute (₹)":
                data_actual = {"Total": actual_total_budget, "Used": actual_used_budget, "Remaining": actual_remaining_budget}
                data_pred = {"Total": predicted_total, "Used": predicted_used, "Remaining": predicted_remaining}
                formatter = format_inr
                ylabel = "₹ Amount"
            else:
                data_actual = {
                    "Used": (actual_used_budget / actual_total_budget) * 100 if actual_total_budget else 0,
                    "Remaining": (actual_remaining_budget / actual_total_budget) * 100 if actual_total_budget else 0
                }
                data_pred = {
                    "Used": (predicted_used / predicted_total) * 100 if predicted_total else 0,
                    "Remaining": (predicted_remaining / predicted_total) * 100 if predicted_total else 0
                }
                formatter = lambda x: f"{x:.1f}%"
                ylabel = "Percentage"

            fig1, ax1 = plt.subplots()
            bar_width = 0.35
            x = range(len(data_actual))
            bars1 = ax1.bar(x, data_actual.values(), width=bar_width, label="Actual", color='skyblue')
            bars2 = ax1.bar([i + bar_width for i in x], data_pred.values(), width=bar_width, label="Predicted", color='orange')

            # Labels
            for b in bars1 + bars2:
                height = b.get_height()
                ax1.text(b.get_x() + b.get_width() / 2, height * 1.01, formatter(height), ha='center', fontsize=8)

            ax1.set_xticks([i + bar_width/2 for i in x])
            ax1.set_xticklabels(data_actual.keys())
            ax1.set_ylabel(ylabel)
            ax1.set_title("Actual vs Predicted Budget")
            ax1.legend()
            ax1.grid(True, linestyle="--", axis="y")
            st.pyplot(fig1)

            # 2️⃣ Pie Chart
            st.subheader("🥧 Pie Chart: Budget Distribution")
            pie_col1, pie_col2 = st.columns(2)

            # Actual Pie
            with pie_col1:
                fig2, ax2 = plt.subplots()
                ax2.pie([actual_used_budget, actual_remaining_budget],
                        labels=["Used", "Remaining"],
                        autopct='%1.1f%%',
                        colors=["#ff9999", "#66b3ff"],
                        startangle=140)
                ax2.set_title("Actual Budget")
                st.pyplot(fig2)

            # Predicted Pie
            with pie_col2:
                fig3, ax3 = plt.subplots()
                ax3.pie([predicted_used, predicted_remaining],
                        labels=["Used", "Remaining"],
                        autopct='%1.1f%%',
                        colors=["#ffcc99", "#99ff99"],
                        startangle=140)
                ax3.set_title("Predicted Budget")
                st.pyplot(fig3)

        except Exception as e:
            st.error(f"❌ Error during prediction or visualization: {e}")
