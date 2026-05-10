import requests

COINGECKO_URL = "https://api.coingecko.com/api/v3/simple/price"
BINANCE_URL = "https://api1.binance.com/api/v3/ticker/price"
HYPERLIQUID_URL = "https://api.hyperliquid.xyz/info"

last_price = None

def get_price(symbol="BTCUSDT"):
    global last_price

    # Map symbols to CoinGecko IDs
    mapping = {
        "BTCUSDT": "bitcoin",
        "ETHUSDT": "ethereum",
        "SOLUSDT": "solana"
    }

    coin_id = mapping.get(symbol, "bitcoin")

    # 1️⃣ Try CoinGecko
    try:
        r = requests.get(COINGECKO_URL, params={"ids": coin_id, "vs_currencies": "usd"}, timeout=2)
        data = r.json()
        price = float(data[coin_id]["usd"])
        last_price = price
        return price
    except:
        pass

    # 2️⃣ Try Binance
    try:
        r = requests.get(BINANCE_URL, params={"symbol": symbol}, timeout=2)
        data = r.json()
        price = float(data["price"])
        last_price = price
        return price
    except:
        pass

    # 3️⃣ Try Hyperliquid
    try:
        r = requests.get(HYPERLIQUID_URL, timeout=2)
        data = r.json()
        price = float(data["markPx"])
        last_price = price
        return price
    except:
        pass

    # 4️⃣ Fallback: return last known price
    return last_price