import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
from data_utils import fetch_market_data, fetch_fred_data, rename_columns

# ------------------ PAGE CONFIG ------------------
st.set_page_config(page_title="Live Market Data", page_icon="🧾", layout="wide")

# ------------------ TITLE ------------------
st.title("📊 Live Market & Economic Data")
st.caption("Showing available data from the last 20 years")

# ------------------ DATE RANGE ------------------
st.sidebar.header("📅 Date Range Selector")

end = datetime.today().date()
start = st.sidebar.date_input(
    "Select Start Date",
    value=end - timedelta(days=365 * 20),
    min_value=end - timedelta(days=365 * 20),
    max_value=end
)

if start >= end:
    st.sidebar.error("Start date must be earlier than end date.")
    st.stop()


# ------------------ YAHOO FINANCE DATA ------------------
st.subheader("💹 Market Data (Yahoo Finance)")

try:
    st.info("Fetching and processing market data...")
    full_market_data = fetch_market_data()
    clean_market_data = rename_columns(full_market_data)

    # Filter data for selected range
    filtered_market = clean_market_data.loc[str(start):str(end)]

    # Display
    st.dataframe(filtered_market, use_container_width=True)
except Exception as e:
    st.error(f"⚠️ Error fetching Yahoo Finance data: {e}")

# ------------------ FRED ECONOMIC DATA ------------------
st.markdown("---")
st.subheader("🏦 Macroeconomic Indicators (FRED)")

try:
    cpi_df, irate_df = fetch_fred_data()
    fred_df = pd.concat([cpi_df, irate_df], axis=1)
    fred_filtered = fred_df.loc[str(start):str(end)]

    st.dataframe(fred_filtered, use_container_width=True)
except Exception as e:
    st.error(f"⚠️ Error fetching FRED data: {e}")

# ------------------ FOOTER ------------------
st.markdown("---")
st.caption("📈 Source: Yahoo Finance (via yfinance) & FRED (Federal Reserve)")
