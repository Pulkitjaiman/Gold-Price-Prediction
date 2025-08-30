# Gold Price Prediction App - Home Page

import streamlit as st
from datetime import datetime

st.set_page_config(page_title="Gold Price Predictor", page_icon="🟡", layout="wide")

# ----------- Hero Banner -----------
st.markdown("""
    <div style='text-align: center; padding: 2rem 1rem; background: linear-gradient(120deg, #f6d365 0%, #fda085 100%); border-radius: 15px;'>
        <h1 style='color: #2c3e50; font-size: 3.2rem;'>🟡 Gold Price Predictor</h1>
        <p style='font-size: 1.4rem; color: #2c3e50;'>Forecast tomorrow’s gold price using real-time market & economic indicators.</p>
    </div>
""", unsafe_allow_html=True)

# ----------- Description -----------
st.markdown("### 📘 Project Overview")
st.markdown("""
Gold prices are impacted by various macroeconomic indicators and market conditions.
This web app allows users to:
- 📈 View latest gold and related market indicators
- 🤖 Predict gold prices using a machine learning model
- 📉 Analyze trends including peaks and troughs
- 📊 Visualize 30-day historical gold data

All data is fetched live from **Yahoo Finance** and **FRED** APIs.
""")

# ----------- How It Works -----------
st.markdown("### 🧠 How the Model Works")
st.markdown("""
The app uses **Linear Regression** trained on the following indicators:
- Previous day's gold closing price
- Crude oil price
- USD index
- S&P 500 index
- Consumer Price Index (CPI)
- Interest rate (FED Funds Rate)

Each day, new data is fetched and a prediction is generated for the next gold close.
""")

# ----------- Navigation CTA -----------
st.markdown("---")
st.markdown("<h3 style='text-align: center;'>🚀 Ready to Get Started?</h3>", unsafe_allow_html=True)

# ✅ Use Streamlit's page switcher
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    if st.button("🔮 Go to Live Prediction"):
        st.switch_page("pages/3_Gold_Predictor.py")  # Make sure the path matches exactly


# ----------- Footer -----------
st.markdown("---")
st.caption(f"🕒 Last Updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
st.caption("Developed using Streamlit | Data from Yahoo Finance & FRED | Model: Linear Regression")
