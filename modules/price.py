import websocket
import json
import threading

latest_price = None

def _run_socket(symbol):
    global latest_price

    stream = f"wss://stream.binance.com:9443/ws/{symbol.lower()}@trade"

    def on_message(ws, message):
        global latest_price
        data = json.loads(message)
        latest_price = float(data["p"])

    ws = websocket.WebSocketApp(stream, on_message=on_message)
    ws.run_forever()

def start_price_stream(symbol="btcusdt"):
    thread = threading.Thread(target=_run_socket, args=(symbol,), daemon=True)
    thread.start()

def get_latest_price():
    return latest_price