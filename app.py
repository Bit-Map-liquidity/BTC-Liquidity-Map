import streamlit as st
import time
import plotly.graph_objects as go

from modules.footprint import start_footprint_stream, get_current_footprint

# ---------------------------------------------------------
# Streamlit Page Setup
# ---------------------------------------------------------
st.set_page_config(
    page_title="BTC Liquidity Dashboard",
    layout="wide"
)

st.title("BTCUSDT — 1‑Minute Footprint (1‑Tick Resolution)")

# ---------------------------------------------------------
# Start WebSocket Footprint Stream
# ---------------------------------------------------------
start_footprint_stream()

# Placeholder for live updates
placeholder = st.empty()

# ---------------------------------------------------------
# Live Update Loop
# ---------------------------------------------------------
while True:
    fp = get_current_footprint()

    if fp is None:
        with placeholder.container():
            st.write("Connecting to footprint stream…")
        time.sleep(0.2)
        continue

    # Extract footprint levels
    levels = sorted(fp["levels"].keys(), reverse=True)
    bids = [fp["levels"][lvl]["bid"] for lvl in levels]
    asks = [fp["levels"][lvl]["ask"] for lvl in levels]

    # ---------------------------------------------------------
    # Build Plotly Footprint Chart
    # ---------------------------------------------------------
    fig = go.Figure()

    # Bid volume (red)
    fig.add_trace(go.Bar(
        x=bids,
        y=levels,
        orientation="h",
        name="Bid Volume",
        marker_color="red",
        opacity=0.6
    ))

    # Ask volume (green)
    fig.add_trace(go.Bar(
        x=asks,
        y=levels,
        orientation="h",
        name="Ask Volume",
        marker_color="green",
        opacity=0.6
    ))

    # Layout
    fig.update_layout(
        height=900,
        barmode="overlay",
        title=f"1‑Minute Footprint — Delta: {fp['delta']:.2f}",
        yaxis_title="Price",
        xaxis_title="Volume",
        template="plotly_dark",
        showlegend=True
    )

    # ---------------------------------------------------------
    # Render in Streamlit
    # ---------------------------------------------------------
    with placeholder.container():
       st.plotly_chart(fig, use_container_width=True, key=str(time.time()))

    # Update speed (5 times per second)
    time.sleep(0.2)