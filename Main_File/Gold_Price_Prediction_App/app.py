import streamlit as st

st.set_page_config(
    page_title="Gold Price Predictor",
    page_icon="🪙",
    layout="wide"
)

# ---------- CSS Styling ----------
st.markdown("""
    <style>
    .stApp {
        background: url("https://cdn.pixabay.com/animation/2023/06/22/13/17/13-17-02-539_512.gif") repeat;
        background-size: cover;
        animation: animate-bg 30s linear infinite;
    }

    @keyframes animate-bg {
        0% { background-position: 0% 0%; }
        100% { background-position: 100% 100%; }
    }

    .header-box {
        background-color: rgba(0, 0, 0, 0.6);
        border-radius: 15px;
        padding: 2rem;
        margin: 2rem auto 1rem auto;
        box-shadow: 0 10px 25px rgba(0, 0, 0, 0.25);
        text-align: center;
        max-width: 900px;
        color: #ffffff;
    }

    .nav-bar {
        text-align: center;
        margin-bottom: 2rem;
    }

    .nav-bar a {
        display: inline-block;
        margin: 0.5rem 0.5rem;
        padding: 0.6rem 1.2rem;
        background-color: #fdd835;
        color: #000;
        text-decoration: none;
        border-radius: 10px;
        font-weight: bold;
        font-size: 1rem;
        transition: background 0.3s ease;
        box-shadow: 0 2px 8px rgba(0,0,0,0.3);
    }

    .nav-bar a:hover {
        background-color: #fbc02d;
        color: black;
    }

    .content-box {
        background-color: rgba(0, 0, 0, 0.65);
        padding: 2rem;
        border-radius: 15px;
        margin: 2rem;
        box-shadow: 0 4px 15px rgba(0,0,0,0.2);
        color: #f1f1f1;
    }

    h1, h2, h3, p, li, strong {
        color: #f9f9f9;
    }

    ul {
        padding-left: 1.5rem;
    }
    </style>
""", unsafe_allow_html=True)

# ---------- Header Section ----------
st.markdown("""
    <div class="header-box">
        <h1>🪙 Gold Price Predictor</h1>
        <p>Accurate forecasting using real-time financial and macroeconomic indicators.</p>
    </div>
""", unsafe_allow_html=True)

# ---------- Navigation Buttons ----------
st.markdown("""
    <div class="nav-bar">
        <a href="/home" target="_self">🏡 Home</a>
        <a href="/Gold_Predictor" target="_self">📈 Gold Predictor</a>
        <a href="/Live_Market_Data" target="_self">📊 Live Market Data</a>
        <a href="/Historical_Analysis" target="_self">📈 Historical Analysis</a>
        <a href="/Model_Info" target="_self">📙 Model Info</a>
        <a href="/About" target="_self">ℹ️ About</a>
    </div>
""", unsafe_allow_html=True)

# ---------- Main Description Content ----------
st.markdown("""
    <div class="content-box">
        <h3>📍 Welcome to the Gold Price Prediction Platform!</h3>
        <p>This platform uses real-time data from financial markets and macroeconomic indicators to predict the price of gold for the next trading day.</p>
        <ul>
            <li>🔎 Track gold, oil, dollar index, and S&P 500</li>
            <li>📈 Predict gold using a live machine learning model</li>
            <li>📤 Upload your own data for instant predictions</li>
            <li>📚 Learn about how the model works and what powers it</li>
        </ul>
        <p><strong>Use the navigation buttons above or the sidebar to explore.</strong></p>
    </div>
""", unsafe_allow_html=True)

# ---------- Footer ----------
st.caption("© 2025 | Made with ❤️ using Streamlit, FRED, and Yahoo Finance APIs")
