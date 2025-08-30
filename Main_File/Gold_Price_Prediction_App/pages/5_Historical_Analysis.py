# Gold Price Prediction App - Historical Analysis Page

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from data_utils import prepare_data

st.set_page_config(page_title="📊 Historical Analysis", page_icon="📈", layout="wide")

st.title("📊 Gold Price Historical Analysis")

# Load data
df = prepare_data().copy()
df = df.reset_index().rename(columns={"index": "Date"})
df.set_index("Date", inplace=True)

# Chart 1: Gold Closing Prices
st.subheader("📈 Gold Closing Prices Over Time")
fig1, ax1 = plt.subplots(figsize=(12,6))
ax1.plot(df.index, df['Gold_Close'], color='gold')
ax1.set_title("Gold Closing Prices Over Time")
ax1.set_xlabel("Date")
ax1.set_ylabel("Gold Price (USD)")
ax1.grid(True)
st.pyplot(fig1)

# Chart 2: Daily % Change
df['Gold_Pct_Change'] = df['Gold_Close'].pct_change() * 100
st.subheader("📉 Daily % Change in Gold Prices")
fig2, ax2 = plt.subplots(figsize=(12,5))
ax2.plot(df.index, df['Gold_Pct_Change'], color='darkred')
ax2.axhline(0, linestyle='--', color='black')
ax2.set_title("Daily % Change in Gold Prices")
ax2.set_xlabel("Date")
ax2.set_ylabel("% Change")
ax2.grid(True)
st.pyplot(fig2)

# Chart 3: Moving Average
df['Gold_30D_MA'] = df['Gold_Close'].rolling(window=30).mean()
st.subheader("📉 30-Day Moving Average")
fig3, ax3 = plt.subplots(figsize=(12,6))
ax3.plot(df.index, df['Gold_Close'], label='Gold Close', color='gold')
ax3.plot(df.index, df['Gold_30D_MA'], label='30-Day MA', color='blue')
ax3.set_title("Gold Price with 30-Day Moving Average")
ax3.set_xlabel("Date")
ax3.set_ylabel("Gold Price (USD)")
ax3.legend()
ax3.grid(True)
st.pyplot(fig3)

# Chart 4: Gold vs USD Index
st.subheader("🪙 Gold vs USD Index")
fig4, ax4 = plt.subplots(figsize=(12,6))
ax4.plot(df.index, df['Gold_Close'], label='Gold Price', color='gold')
ax4.plot(df.index, df['USDIndex_Close'], label='USD Index', color='green')
ax4.set_title("Gold vs USD Index")
ax4.legend()
ax4.grid(True)
st.pyplot(fig4)

# Chart 5: Gold vs Crude Oil
st.subheader("🛢️ Gold vs Crude Oil")
fig5, ax5 = plt.subplots(figsize=(12,6))
ax5.plot(df.index, df['Gold_Close'], label='Gold Price', color='gold')
ax5.plot(df.index, df['CrudeOil_Close'], label='Crude Oil Price', color='brown')
ax5.set_title("Gold vs Crude Oil")
ax5.legend()
ax5.grid(True)
st.pyplot(fig5)

# Chart 6: Gold vs S&P 500
st.subheader("📊 Gold vs S&P 500 Index")
fig6, ax6 = plt.subplots(figsize=(12,6))
ax6.plot(df.index, df['Gold_Close'], label='Gold Price', color='gold')
ax6.plot(df.index, df['SP500_Close'], label='S&P 500', color='blue')
ax6.set_title("Gold vs S&P 500")
ax6.legend()
ax6.grid(True)
st.pyplot(fig6)

# Correlation Heatmap
st.subheader("📈 Correlation Heatmap")
cols_of_interest = ['Gold_Close', 'USDIndex_Close', 'CrudeOil_Close', 'SP500_Close', 'Interest_Rate', 'CPI']
corr_matrix = df[cols_of_interest].corr()
fig7, ax7 = plt.subplots(figsize=(10,6))
sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', ax=ax7)
ax7.set_title("Correlation Heatmap: Gold vs Economic Indicators")
st.pyplot(fig7)


# Final Note
st.markdown("---")
