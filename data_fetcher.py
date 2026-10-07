import requests
import pandas as pd

def get_historical_data(coin_id="bitcoin", days=90, currency="usd"):
    """
    دریافت داده‌های تاریخی قیمت از CoinGecko
    """
    url = f"https://api.coingecko.com/api/v3/coins/{coin_id}/market_chart"
    params = {
        "vs_currency": currency,
        "days": days,
        "interval": "daily"
    }
    
    response = requests.get(url, params=params)
    response.raise_for_status()
    data = response.json()
    
    prices = data["prices"]
    df = pd.DataFrame(prices, columns=["timestamp", "price"])
    df["date"] = pd.to_datetime(df["timestamp"], unit="ms")
    df = df[["date", "price"]]
    return df

def get_current_price(coin_id="bitcoin", currency="usd"):
    url = f"https://api.coingecko.com/api/v3/simple/price"
    params = {"ids": coin_id, "vs_currencies": currency}
    response = requests.get(url, params=params)
    response.raise_for_status()
    return response.json()[coin_id][currency]
