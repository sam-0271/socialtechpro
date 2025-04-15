import streamlit as st

# Page config
st.set_page_config(
    page_title="Smart Complaint System",
    page_icon="📣",
    layout="wide"
)

# -------------------- Welcome Section --------------------
st.markdown("""
    <div style='background-color: #f2f6fc; padding: 30px 40px; border-radius: 12px; box-shadow: 0 2px 10px rgba(0, 0, 0, 0.05); margin-bottom: 30px;'>
        <h1 style='font-size: 36px;'>📣 Welcome to the Smart Complaint Management System</h1>
        <p style='font-size: 18px; margin-top: 20px;'>This system uses <b>AI</b> & <b>Machine Learning</b> to:</p>
        <ul style='font-size: 17px; line-height: 1.6;'>
            <li>📂 Classify complaints</li>
            <li>🏢 Assign departments</li>
            <li>⏱️ Predict resolution time</li>
            <li>💰 Estimate budget usage</li>
        </ul>
        <p style='margin-top: 20px; font-size: 17px;'>👉 Use the <b>sidebar</b> to navigate through the steps.</p>
    </div>
""", unsafe_allow_html=True)

# -------------------- Feature Cards --------------------
col1, col2 = st.columns(2)

with col1:
    st.markdown(
        """
        <div style='background-color: white; padding: 20px; border-radius: 12px; box-shadow: 0 2px 8px rgba(0,0,0,0.06); margin-bottom: 20px;'>
            <h4>📂 Complaint Classification</h4>
            <p>Automatically categorize complaints using Natural Language Processing.</p>
        </div>
        """,
        unsafe_allow_html=True
    )
    st.markdown(
        """
        <div style='background-color: white; padding: 20px; border-radius: 12px; box-shadow: 0 2px 8px rgba(0,0,0,0.06);'>
            <h4>⏱️ Predict Resolution Time</h4>
            <p>Estimate resolution time based on complaint category and past data trends.</p>
        </div>
        """,
        unsafe_allow_html=True
    )

with col2:
    st.markdown(
        """
        <div style='background-color: white; padding: 20px; border-radius: 12px; box-shadow: 0 2px 8px rgba(0,0,0,0.06); margin-bottom: 20px;'>
            <h4>🏢 Department Assignment</h4>
            <p>Automatically assign complaints to the most relevant department.</p>
        </div>
        """,
        unsafe_allow_html=True
    )
    st.markdown(
        """
        <div style='background-color: white; padding: 20px; border-radius: 12px; box-shadow: 0 2px 8px rgba(0,0,0,0.06);'>
            <h4>💰 Budget Forecasting</h4>
            <p>Predict budget usage based on complaint volume and resource allocation.</p>
        </div>
        """,
        unsafe_allow_html=True
    )

# -------------------- Future Complaints Prediction --------------------
st.markdown("---")
st.subheader("🔮 Future Complaints Prediction")

st.markdown(
    """
    <div style='background-color: #fff9ed; padding: 25px; border-left: 6px solid #f39c12; border-radius: 10px; margin-top: 10px;'>
        <p style='font-size: 17px;'>
        The <strong>Future Complaints Prediction</strong> module uses historical data and machine learning models 
        to predict how many complaints may be handled by a department in future months.
        </p>
        <ul style='font-size: 16px; line-height: 1.6;'>
            <li>📊 Forecast departmental workload</li>
            <li>📅 Plan staffing and resource needs in advance</li>
            <li>📈 Improve operational efficiency with predictive insights</li>
        </ul>
        <p style='font-size: 17px;'>🚀 Access this module from the sidebar to explore future trends and take proactive actions!</p>
    </div>
    """,
    unsafe_allow_html=True
)

# -------------------- Footer --------------------
st.markdown("---")
st.markdown("<center>🚀 Made with ❤️ using Python & Streamlit</center>", unsafe_allow_html=True)
