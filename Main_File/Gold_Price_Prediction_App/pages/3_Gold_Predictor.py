import pandas as pd
import streamlit as st
from datetime import datetime, timedelta
from data_utils import (
    prepare_data,
    load_or_train_model,
    get_latest_inputs,
    predict_next_price,
    get_peak_and_trough,
    fetch_market_data,
    rename_columns,
    compare_models
)

# ----------------- Page Configuration -----------------
st.set_page_config(page_title="Gold Price Predictor", page_icon="📈", layout="wide")
st.markdown("## 📈 Real-Time Gold Price Prediction")
st.caption("Powered by live financial and macroeconomic indicators")
st.markdown("---")

# ----------------- Prediction Mode -----------------
st.markdown("### ⚙️ Select the Data Input Mode")
mode = st.radio(
    "Choose how to input today's market indicators:",
    ["-- Select Mode --", "🔁 Auto Fetch (Recommended)", "✍️ Manual Entry"],
    index=0
)

if mode == "-- Select Mode --":
    st.warning("Please select a prediction mode to continue.")
    st.stop()

# ----------------- Collect Inputs -----------------
features, last_close, last_high, pred_date = None, None, None, None
submitted = False

if mode == "✍️ Manual Entry":
    _, last_close, last_high, pred_date = get_latest_inputs()

    st.markdown("### ✍️ Enter the Price for Market Indicators Manually")
    with st.form("manual_form"):
        col1, col2 = st.columns(2)
        with col1:
            prev_gold = st.number_input("🪙 Previous Gold Close ($)", min_value=0.0, format="%.2f")
            prev_high = st.number_input("🔺 Previous Gold High ($)", min_value=0.0, format="%.2f")
            sp500 = st.number_input("📈 S&P 500", min_value=0.0, format="%.2f")
            dow = st.number_input("📊 Dow Jones", min_value=0.0, format="%.2f")
            euro = st.number_input("💶 Euro", min_value=0.0, format="%.2f")
            stoxx = st.number_input("🇪🇺 Euro Stoxx", min_value=0.0, format="%.2f")
            crude = st.number_input("🛢 Crude Oil", min_value=0.0, format="%.2f")
            apple = st.number_input("🍎 Apple", min_value=0.0, format="%.2f")
        with col2:
            bonds = st.number_input("💸 US Bonds (10Y)", min_value=0.0, format="%.2f")
            bank = st.number_input("🏦 US Bank ETF", min_value=0.0, format="%.2f")
            plat = st.number_input("🔘 Platinum", min_value=0.0, format="%.2f")
            pall = st.number_input("⚪ Palladium", min_value=0.0, format="%.2f")
            miners = st.number_input("🛠 Gold Miners ETF", min_value=0.0, format="%.2f")
            usoil = st.number_input("🛢 US Oil ETF", min_value=0.0, format="%.2f")
            usd = st.number_input("💵 USD Index", min_value=0.0, format="%.2f")
            cpi = st.number_input("📊 CPI (Inflation)", min_value=0.0, format="%.2f")
            irate = st.number_input("🏦 Interest Rate (%)", min_value=0.0, format="%.2f")
        submitted = st.form_submit_button("✅ Continue")

    if not submitted:
        st.info("Please enter the values and click **Continue** to proceed.")
        st.stop()
    else:
        features = {
            'Prev_Gold_Close': float(prev_gold),
            'Prev_Gold_High': float(prev_high),
            'SP500_Close': float(sp500),
            'DowJones_Close': float(dow),
            'Euro_Close': float(euro),
            'EuroStoxx_Close': float(stoxx),
            'CrudeOil_Close': float(crude),
            'Apple_Close': float(apple),
            'USBonds10Y_Close': float(bonds),
            'USBankETF_Close': float(bank),
            'Platinum_Close': float(plat),
            'Palladium_Close': float(pall),
            'GoldMinersETF_Close': float(miners),
            'USOilETF_Close': float(usoil),
            'USDIndex_Close': float(usd),
            'CPI': float(cpi),
            'Interest_Rate': float(irate)
        }

else:
    with st.spinner("Fetching today's indicators..."):
        try:
            features, last_close, last_high, pred_date = get_latest_inputs()
        except Exception as e:
            st.error("❌ Failed to fetch real-time indicators.")
            st.exception(e)
            st.stop()

# ----------------- Model Selection -----------------
st.markdown("### 🧠 Auto-Selecting the Best Model")
with st.spinner("Comparing models based on accuracy..."):
    try:
        df = prepare_data()
        best_model_type, model_scores = compare_models(df)
        model_close = load_or_train_model(df, best_model_type, target="Close")
        model_high = load_or_train_model(df, best_model_type, target="High")
        st.success(f"✅ Selected Best Model: {best_model_type}")
    except Exception as e:
        st.error("❌ Model comparison or loading failed.")
        st.exception(e)
        st.stop()

# ----------------- Load Models -----------------
@st.cache_resource
def get_models(model_type):
    df = prepare_data()
    model_close = load_or_train_model(df, model_type, target="Close")
    model_high = load_or_train_model(df, model_type, target="High")
    return df, model_close, model_high

with st.spinner(f"Loading {best_model_type} models and historical data..."):
    try:
        df, model_close, model_high = get_models(best_model_type)
        st.success("✅ Models loaded.")
    except Exception as e:
        st.error("❌ Failed to load models or data.")
        st.exception(e)
        st.stop()

# ----------------- Run Predictions -----------------
with st.spinner("Running predictions..."):
    try:
        predicted_close = predict_next_price(features, model_close)
        predicted_high = predict_next_price(features, model_high)
    except Exception as e:
        st.error("❌ Prediction failed.")
        st.exception(e)
        st.stop()

# ----------------- Peak/Trough -----------------
st.markdown("### 📉 Gold Price Trends")
window = st.slider("Select window for trend analysis (days)", 10, 90, 30)
peak, trough, peak_date, trough_date, gold_df = get_peak_and_trough(pred_date, window)

# ----------------- Display Indicators -----------------
st.subheader("🟡 Today's Key Market Indicators")
col1, col2 = st.columns(2)
with col1:
    st.metric("🪙 Gold (Last Close)", f"${last_close:.2f}")
    st.metric("🔺 Gold (Last High)", f"${last_high:.2f}")
    st.metric("🛢 Crude Oil", f"${features['CrudeOil_Close']:.2f}")
    st.metric("💵 USD Index", f"{features['USDIndex_Close']:.2f}")
with col2:
    st.metric("📈 S&P 500", f"{features['SP500_Close']:.2f}")
    st.metric("📊 CPI (Inflation)", f"{features['CPI']:.2f}")
    st.metric("🏦 Interest Rate", f"{features['Interest_Rate']:.2f} %")

st.markdown("---")

# ----------------- Extra Market Indicators -----------------
st.subheader("📌 Other Market Indicators (Today's Close)")
try:
    full_market_data = fetch_market_data()
    cleaned_market_data = rename_columns(full_market_data)
    latest_row = cleaned_market_data.iloc[-1]

    excluded = ['Gold_Close', 'Gold_High', 'CrudeOil_Close', 'USDIndex_Close', 'SP500_Close']
    close_cols = [col for col in latest_row.index if col.endswith("_Close") and col not in excluded]

    extra_data = pd.DataFrame(latest_row[close_cols])
    extra_data.columns = ["Close Price"]
    extra_data.index.name = "Asset"
    st.dataframe(extra_data.style.format({"Close Price": "${:.2f}"}), use_container_width=True)
except Exception as e:
    st.warning("⚠️ Could not fetch additional indicators.")
    st.exception(e)

# ----------------- Prediction Output -----------------
st.subheader(f"🔮 Predictions Using {best_model_type}")
today_str = datetime.now().strftime("%A, %B %d, %Y")
tomorrow = pred_date + timedelta(days=1)
tomorrow_str = tomorrow.strftime("%A, %B %d, %Y")

st.write(f"📅 **Today**: `{today_str}`")
st.write(f"📈 **Prediction for Tomorrow**: `{tomorrow_str}`")

col1, col2, col3 = st.columns(3)
delta_close = predicted_close - last_close
delta_high = predicted_high - last_high

if peak and trough:
    col1.metric(f"🔼 {window}-Day Peak", f"${peak:.2f}", f"on {peak_date}")
    col2.metric(f"🔽 {window}-Day Trough", f"${trough:.2f}", f"on {trough_date}")
else:
    col1.metric(f"🔼 {window}-Day Peak", "N/A")
    col2.metric(f"🔽 {window}-Day Trough", "N/A")

col3.metric("🎯 Predicted Close", f"${predicted_close:.2f}", f"{delta_close:+.2f}")
st.metric("📊 Predicted Peak (High)", f"${predicted_high:.2f}", f"{delta_high:+.2f}")

# ----------------- Chart -----------------
with st.expander(f"📈 View Historical {window}-Day Gold Trend"):
    if not gold_df.empty:
        st.line_chart(gold_df['Gold_Close'])
        st.caption(f"Showing the last {window} days of gold futures closing prices.")
    else:
        st.warning("Historical gold price data is not available.")

# ----------------- Footer -----------------
st.markdown("---")
st.caption(
    f"📊 Models: {best_model_type} • Data: Yahoo Finance & FRED • "
    "App built with ❤️ using Streamlit by Team B"
)
