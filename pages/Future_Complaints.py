import streamlit as st
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import LabelEncoder
import matplotlib.pyplot as plt

# Load dataset
df = pd.read_csv('formatted_fiscal_logs_updated.csv')

# Convert 'month' column like 'Jan-24' to numeric month (1 for Jan, 2 for Feb, etc.)
df['month'] = pd.to_datetime(df['month'], format='%b-%y', errors='coerce')
df = df.dropna(subset=['month'])  # Drop rows where conversion failed
df['month'] = df['month'].dt.month

# Encode categorical features
area_encoder = LabelEncoder()
department_encoder = LabelEncoder()

df['area_encoded'] = area_encoder.fit_transform(df['area'])
df['department_encoded'] = department_encoder.fit_transform(df['department'])

# Define features and target
X = df[['area_encoded', 'department_encoded', 'month', 'total_spent', 'avg_cost', 'performance_percentage']]
y = df['complaints_handled']

# Train the model
model = RandomForestRegressor(n_estimators=100, random_state=42)
model.fit(X, y)

# Streamlit UI Setup
st.set_page_config(page_title="Complaints Prediction", layout="centered")
st.title("🔮 Predict Future Complaints Handled by Department")

# Sidebar input section
st.sidebar.header("Input Parameters")
area_input = st.sidebar.selectbox("Select Area", df['area'].unique())
department_input = st.sidebar.selectbox("Select Department", df['department'].unique())
month_input = st.sidebar.number_input("Enter Month (1 = January, 12 = December)", min_value=1, max_value=12, value=3)
total_spent_input = st.sidebar.number_input("Enter Total Spent (₹)", min_value=0, value=500000)
avg_cost_input = st.sidebar.number_input("Enter Average Cost (₹)", min_value=0.0, value=1500.0)
performance_percentage_input = st.sidebar.number_input("Enter Performance Percentage (%)", min_value=0, max_value=100, value=85)

# Transform input features for prediction
area_encoded = area_encoder.transform([area_input])[0]
department_encoded = department_encoder.transform([department_input])[0]

input_data = pd.DataFrame({
    'area_encoded': [area_encoded],
    'department_encoded': [department_encoded],
    'month': [month_input],
    'total_spent': [total_spent_input],
    'avg_cost': [avg_cost_input],
    'performance_percentage': [performance_percentage_input]
})

# Predict
predicted_complaints = model.predict(input_data)[0]

# Display result
st.subheader(f"Predicted Complaints Handled: {predicted_complaints:.2f}")

# Visualization: Predicted Complaints
# Visualization: Predicted Complaints
st.subheader("📊Prediction Visualization")

fig, ax = plt.subplots(figsize=(10, 5))

# Use gradient color for the bar
from matplotlib.patches import Rectangle
from matplotlib.colors import LinearSegmentedColormap

# Define custom colormap
cmap = LinearSegmentedColormap.from_list("green_gradient", ["#a8e6cf", "#56c596", "#379683"])

# Plotting a single fancy bar
bar = ax.barh(
    [department_input],
    [predicted_complaints],
    color=cmap(0.6),
    edgecolor='#2f4858',
    height=0.6
)

# Add glow effect using multiple translucent rectangles
for i in range(1, 4):
    ax.barh(
        [department_input],
        [predicted_complaints],
        color=cmap(0.6),
        alpha=0.15 / i,
        height=0.6 + i * 0.2
    )

# Add predicted value as label
ax.text(
    predicted_complaints + 2,
    0,
    f"{predicted_complaints:.2f} 🚀",
    va='center',
    fontsize=14,
    fontweight='bold',
    color='#333'
)

# Style adjustments
ax.set_xlim(0, max(100, predicted_complaints + 20))
ax.set_facecolor('#f7f9fb')
fig.patch.set_facecolor('#f7f9fb')
ax.set_xlabel("Predicted Complaints", fontsize=12, labelpad=10)
ax.set_title("🌟 Predicted Complaints Handled by Department", fontsize=16, weight='bold', pad=15)
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.spines['left'].set_color('#aaa')
ax.spines['bottom'].set_color('#aaa')
ax.tick_params(colors='#666')

st.pyplot(fig)
