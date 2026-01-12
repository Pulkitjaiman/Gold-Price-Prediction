# Gold Price Prediction App - About Page

import streamlit as st

st.set_page_config(page_title="About | Gold Predictor", page_icon="ℹ️", layout="wide")

# --------- Header Styling ----------
st.markdown("""
    <style>
    .header-box {
        background: linear-gradient(to right, #ffd194, #70e1f5);
        padding: 2rem;
        border-radius: 15px;
        text-align: center;
        margin-bottom: 2rem;
    }
    .header-box h1 {
        color: #222;
        font-size: 2.8rem;
    }
    .header-box p {
        color: #333;
        font-size: 1.2rem;
    }
    </style>
    <div class="header-box">
        <h1>ℹ️ About This Project</h1>
        <p>Explore how we use real-time data and machine learning to forecast gold prices with accuracy and transparency.</p>
    </div>
""", unsafe_allow_html=True)

# ---------- Project Overview ----------
st.subheader("📌 Project Overview")
st.markdown("""
This application predicts **next-day gold prices** using real-time **financial market data** and **economic indicators**.  
It is designed to help investors, analysts, and students explore the impact of macro-financial variables on commodity pricing.

**Key Highlights:**
- 🧠 Machine Learning models trained on 20 years of historical data
- 📊 Real-time indicators from Yahoo Finance and FRED
- 🔍 Peak & Trough trend detection
- 📈 Side-by-side model comparison and evaluation
""")

# ---------- Model Highlights ----------
st.subheader("🧠 Machine Learning Models Used")
st.markdown("""
We utilize multiple regression models to predict the **next day's gold closing price**:

- **Linear Regression**: Simple and interpretable  
- **Random Forest Regressor**: Robust and handles nonlinearities  
- **Support Vector Regressor (SVR)**: Good at modeling complex patterns

> ⚙️ Models are trained using features such as:
- Previous Gold Close & High
- Crude Oil, USD Index, S&P 500, Dow Jones, Euro, EuroStoxx
- Platinum, Palladium, Apple Stock, US Bonds & Banks
- CPI (Inflation) and Interest Rates from FRED
""")

# ---------- Data Sources ----------
st.subheader("🔗 Data Sources")
st.markdown("""
- **📉 Yahoo Finance API**  
  ▫ Gold Futures (`GC=F`)  
  ▫ S&P 500 (`^GSPC`), Dow Jones (`^DJI`)  
  ▫ Crude Oil (`CL=F`), USD Index (`DX-Y.NYB`)  
  ▫ Apple (`AAPL`), Euro (`EUR=X`), EuroStoxx (`^STOXX50E`)  
  ▫ Bonds (`^TNX`), Banks ETF (`KBE`), GDX, PL=F, PA=F, USO  

- **📊 FRED API (Federal Reserve Economic Data)**  
  ▫ Inflation Rate (CPI): [CPIAUCSL](https://fred.stlouisfed.org/series/CPIAUCSL)  
  ▫ Interest Rate (Fed Funds): [FEDFUNDS](https://fred.stlouisfed.org/series/FEDFUNDS)
""")

# ---------- Additional Notes ----------
st.subheader("📚 How It Works")
st.markdown("""
- Data is fetched live using Yahoo Finance & FRED  
- Features like lag values, moving averages, and economic indicators are created  
- Models are trained or loaded from saved files  
- The system predicts the next day's gold **closing** and **high** price  
- We also analyze **past 30-day trends** to detect **peak and trough prices**
""")

# ---------- Footer ----------
st.markdown("---")
st.caption("Built using Streamlit | Powered by Yahoo Finance and FRED APIs | © 2025")
