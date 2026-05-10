import requests

COINGECKO_URL = "https://api.coingecko.com/api/v3/simple/price"

def get_price(symbol="BTCUSDT"):
    try:
        # Map trading pairs to CoinGecko IDs
        mapping = {
            "BTCUSDT": "bitcoin",
            "ETHUSDT": "ethereum",
            "SOLUSDT": "solana"
        }

        coin_id = mapping.get(symbol, "bitcoin")

        response = requests.get(COINGECKO_URL, params={
            "ids": coin_id,
            "vs_currencies": "usd"
        })

        data = response.json()
        return float(data[coin_id]["usd"])
    except Exception:
        return None