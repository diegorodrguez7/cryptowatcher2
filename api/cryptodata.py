from fastapi import FastAPI
from fastapi.responses import JSONResponse
import requests

app = FastAPI()

COINS = ["bitcoin", "ethereum"]

def fetch_price(coin):
    url = f"https://api.coingecko.com/api/v3/coins/{coin}"
    res = requests.get(url)
    data = res.json()
    current_price = data["market_data"]["current_price"]["usd"]
    price_24h = data["market_data"]["price_change_percentage_24h"]
    price_7d = data["market_data"]["price_change_percentage_7d"]
    volume = data["market_data"]["total_volume"]["usd"]
    return {
        "name": coin.capitalize(),
        "price_usd": current_price,
        "change_24h": price_24h,
        "change_7d": price_7d,
        "volume": volume,
        "advice": generate_advice(price_7d, price_24h)
    }

def generate_advice(change_7d, change_24h):
    if change_7d <= -10:
        return "Buena oportunidad de entrada (DCA)."
    elif change_24h > 5:
        return "Alta volatilidad, cuidado con entradas impulsivas."
    elif -1 < change_24h < 1:
        return "Mercado estable, espera una señal clara."
    elif change_24h > 0 and change_7d > 0:
        return "Tendencia positiva, posible continuación alcista."
    else:
        return "Sigue acumulando si crees en el proyecto."

@app.get("/api/prices")
def get_prices():
    data = [fetch_price(coin) for coin in COINS]
    return JSONResponse(content=data)
