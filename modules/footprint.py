import websocket
import json
import threading
import time
from collections import defaultdict

# Thread-safe storage
current_candle = None
completed_candles = []
lock = threading.Lock()

def _new_empty_candle(start_ts):
    return {
        "start_ts": start_ts,
        "open": None,
        "high": None,
        "low": None,
        "close": None,
        "levels": defaultdict(lambda: {"bid": 0.0, "ask": 0.0}),
        "volume": 0.0,
        "delta": 0.0
    }

def _run_socket():
    global current_candle, completed_candles

    stream = "wss://stream.binance.com:9443/ws/btcusdt@trade"

    def on_message(ws, message):
        global current_candle, completed_candles

        data = json.loads(message)
        price = float(data["p"])
        qty = float(data["q"])
        ts = int(data["T"]) // 1000  # convert ms → seconds
        is_sell = data["m"]          # True = sell (hit bid), False = buy (hit ask)

        minute_start = ts - (ts % 60)

        with lock:
            # Create new candle if needed
            if current_candle is None or current_candle["start_ts"] != minute_start:
                if current_candle is not None:
                    completed_candles.append(current_candle)
                current_candle = _new_empty_candle(minute_start)

            c = current_candle

            # Update OHLC
            if c["open"] is None:
                c["open"] = price
            c["close"] = price
            c["high"] = price if c["high"] is None else max(c["high"], price)
            c["low"] = price if c["low"] is None else min(c["low"], price)

            # Update footprint levels
            level = round(price, 2)  # 1‑tick resolution
            if is_sell:
                c["levels"][level]["bid"] += qty
                c["delta"] -= qty
            else:
                c["levels"][level]["ask"] += qty
                c["delta"] += qty

            # Update volume
            c["volume"] += qty

    ws = websocket.WebSocketApp(stream, on_message=on_message)
    ws.run_forever()

def start_footprint_stream():
    thread = threading.Thread(target=_run_socket, daemon=True)
    thread.start()

def get_current_footprint():
    with lock:
        return current_candle.copy() if current_candle else None

def get_last_n_candles(n):
    with lock:
        return completed_candles[-n:].copy()