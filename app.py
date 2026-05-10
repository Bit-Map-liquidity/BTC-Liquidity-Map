import streamlit as st
import time
from modules.price import get_price

st.set_page_config(page_title="BTC Liquidity Dashboard", layout="wide")

# Sidebar
st.sidebar.title("Settings")
symbol = st.sidebar.selectbox("Select Symbol", ["BTCUSDT", "ETHUSDT", "SOLUSDT"])

# Main Title
st.title("BTC Liquidity Dashboard")

# Live Price Section
st.subheader(f"Live Price — {symbol}")

price = get_price(symbol)

if price:
    st.metric(label="Current Price", value=f"${price:,.2f}")
else:
    st.error("Failed to fetch price")

# Auto-refresh every 5 seconds
time.sleep(5)
st.experimental_rerun()