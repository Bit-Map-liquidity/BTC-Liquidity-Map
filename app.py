import streamlit as st
import time
from modules.price import start_price_stream, get_latest_price

st.set_page_config(page_title="BTC Liquidity Dashboard", layout="wide")

# Sidebar
st.sidebar.title("Settings")
symbol = st.sidebar.selectbox("Select Symbol", ["BTCUSDT", "ETHUSDT", "SOLUSDT"])

# Start WebSocket stream
start_price_stream(symbol)

st.title("BTC Liquidity Dashboard")

placeholder = st.empty()

while True:
    with placeholder.container():
        st.subheader(f"Live Price — {symbol}")

        price = get_latest_price()

        if price:
            st.metric("Current Price", f"${price:,.2f}")
        else:
            st.write("Connecting to live price feed...")

    time.sleep(0.2)  # update 5 times per second