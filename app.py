import streamlit as st
import time
import plotly.graph_objects as go

from modules.footprint import (
    start_footprint_stream,
    get_current_footprint,
    get_last_n_candles
)

# ---------------------------------------------------------
# Streamlit Page Setup
# ---------------------------------------------------------
st.set_page_config(
    page_title="BTC Footprint",
    layout="wide"
)

st.title("BTCUSDT — 1‑Minute Footprint (Multi‑Candle View)")

# Start WebSocket footprint stream
start_footprint_stream()

placeholder = st.empty()

# Number of candles to show on screen
NUM_CANDLES = 20

# ---------------------------------------------------------
# Live Update Loop
# ---------------------------------------------------------
while True:
    current = get_current_footprint()
    history = get_last_n_candles(NUM_CANDLES)

    if current is None:
        with placeholder.container():
            st.write("Connecting to footprint stream…")
        time.sleep(0.2)
        continue

    # Combine history + current candle
    candles = history + [current]

    # ---------------------------------------------------------
    # Build multi‑candle footprint chart
    # ---------------------------------------------------------
    fig = go.Figure()

    # Each candle gets its own x‑offset
    for i, candle in enumerate(candles):
        levels = sorted(candle["levels"].keys(), reverse=True)
        bids = [candle["levels"][lvl]["bid"] for lvl in levels]
        asks = [candle["levels"][lvl]["ask"] for lvl in levels]

        # Offset each candle horizontally
        x_bids = [i - 0.3] * len(levels)
        x_asks = [i + 0.3] * len(levels)

        # Bid blocks (left side)
        fig.add_trace(go.Bar(
            x=x_bids,
            y=levels,
            orientation="h",
            width=0.6,
            marker_color="red",
            opacity=0.6,
            name="Bid" if i == 0 else "",
            customdata=bids,
            hovertemplate="Bid Vol: %{customdata}<extra></extra>"
        ))

        # Ask blocks (right side)
        fig.add_trace(go.Bar(
            x=x_asks,
            y=levels,
            orientation="h",
            width=0.6,
            marker_color="green",
            opacity=0.6,
            name="Ask" if i == 0 else "",
            customdata=asks,
            hovertemplate="Ask Vol: %{customdata}<extra></extra>"
        ))

    # ---------------------------------------------------------
    # Layout
    # ---------------------------------------------------------
    fig.update_layout(
        height=900,
        barmode="overlay",
        title="1‑Minute Footprint — Multi‑Candle View",
        xaxis=dict(
            tickmode="array",
            tickvals=list(range(len(candles))),
            ticktext=[f"Candle {i+1}" for i in range(len(candles))],
        ),
        yaxis_title="Price",
        template="plotly_dark",
        showlegend=True
    )

    # ---------------------------------------------------------
    # Render
    # ---------------------------------------------------------
    with placeholder.container():
        st.plotly_chart(fig, use_container_width=True, key=str(time.time()))

    time.sleep(0.2)
