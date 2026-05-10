import requests

BINANCE_PRICE_URL = "https://api.binance.com/api/v3/ticker/price"

def get_price(symbol="BTCUSDT"):
    try:
        response = requests.get(BINANCE_PRICE_URL, params={"symbol": symbol})
        data = response.json()
        return float(data["price"])
    except Exception:
        return None