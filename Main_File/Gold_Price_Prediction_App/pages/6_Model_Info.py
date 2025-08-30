# Gold Price Prediction App - Model Info Page

import streamlit as st

st.set_page_config(page_title="Model Info", page_icon="📚", layout="wide")

st.title("📚 Gold Price Predictor – Model Info")
st.markdown("---")

# -------- Model Overview --------
st.header("🧠 Model Overview")
st.markdown("""
This app supports multiple models to predict the **next-day closing price** of **Gold Futures**:

**Available Models**:
- **Linear Regression**: Interpretable, fast, good for linear relationships
- **Random Forest**: Handles complex non-linear interactions and reduces overfitting
- **SVR (Support Vector Regression)**: Useful for small datasets and non-linear regression

These models are trained using real-time financial data from **Yahoo Finance** and macroeconomic indicators from **FRED**.
""")

# -------- Feature Engineering --------
st.header("🔧 Features Used for Prediction")
st.markdown("""
The models use the following market and economic indicators:

| Feature                  | Description                                         |
|--------------------------|-----------------------------------------------------|
| `Prev_Gold_Close`        | Previous day's gold closing price                  |
| `Prev_Gold_High`         | Previous day's gold high price                     |
| `SP500_Close`            | S&P 500 Index (^GSPC)                              |
| `DowJones_Close`         | Dow Jones Index (^DJI)                             |
| `Euro_Close`             | EUR to USD exchange rate                          |
| `EuroStoxx_Close`        | Euro Stoxx 50 Index (^STOXX50E)                    |
| `CrudeOil_Close`         | Crude Oil Futures (CL=F)                           |
| `Apple_Close`            | Apple Inc. Stock Price (AAPL)                     |
| `USBonds10Y_Close`       | 10-Year Treasury Yield (^TNX)                     |
| `USBankETF_Close`        | US Bank ETF (KBE)                                 |
| `Platinum_Close`         | Platinum Futures (PL=F)                            |
| `Palladium_Close`        | Palladium Futures (PA=F)                           |
| `GoldMinersETF_Close`    | Gold Miners ETF (GDX)                              |
| `USOilETF_Close`         | US Oil ETF (USO)                                  |
| `USDIndex_Close`         | US Dollar Index (DX-Y.NYB)                         |
| `CPI`                    | Consumer Price Index (CPIAUCSL from FRED)          |
| `Interest_Rate`          | Federal Funds Rate (FEDFUNDS from FRED)            |
""")

# -------- Training Details --------
st.header("📈 Model Training")
st.markdown("""
- **Training Data Range**: Last 20 years of daily market and macroeconomic data
- **Target Variable**: `Gold_Close` – next day's gold closing price
- **Data Sources**:
  - 🟡 Yahoo Finance for gold, stocks, commodities
  - 🏦 FRED for CPI and Interest Rate
- **Tech Stack**:
  - Python, Pandas, NumPy, Scikit-learn, joblib
- **Saved Models**:
  - `model_Linear_Regression_Close.pkl`
  - `model_Random_Forest_Close.pkl`
  - `model_SVR_Close.pkl`
""")

# -------- Limitations --------
st.header("⚠️ Model Limitations")
st.markdown("""
- Models assume historical market relationships remain consistent in the short term
- They do **not** incorporate breaking news, geopolitical events, or market sentiment
- **SVR** may struggle with volatility; **Random Forest** is more robust

**Future Upgrades**:
- Add **XGBoost** or **Neural Networks (LSTM)** for sequence learning
- Include **Volatility Index (VIX)**, **ETF Flows**, and **Social Media Sentiment**
- Ensemble and hybrid models for improved generalization
""")

# -------- Footer --------
st.markdown("---")
st.caption("Developed by Team B | Powered by Yahoo Finance, FRED, and Scikit-learn")
