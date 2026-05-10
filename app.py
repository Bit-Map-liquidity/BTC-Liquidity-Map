import streamlit as st
import time
from modules.price import get_price

st.set_page_config(page_title="BTC Liquidity Dashboard", layout="wide")

# Sidebar
st.sidebar.title("Settings")
symbol = st.sidebar.selectbox("Select Symbol", ["BTCUSDT", "ETHUSDT", "SOLUSDT"])

# Main Title
st.title("BTC Liquidity Dashboard")

# Create a placeholder container for live updates
placeholder = st.empty()

while True:
    with placeholder.container():
        st.subheader(f"Live Price — {symbol}")

        price = get_price(symbol)

        if price:
            st.metric(label="Current Price", value=f"${price:,.2f}")
        else:
            st.error("Failed to fetch price")

    time.sleep(5)