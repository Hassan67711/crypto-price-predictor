import requests
from datetime import datetime, timedelta

def get_price_data(coin="bitcoin", days=30):
    url = f"https://api.coingecko.com/api/v3/coins/{coin}/market_chart"
    params = {
        "vs_currency": "usd",
        "days": days,
        "interval": "daily"
    }
    response = requests.get(url, params=params)
    data = response.json()
    prices = [item[1] for item in data["prices"]]
    return prices

def simple_predict(prices, days_ahead=7):
    # میانگین متحرک ساده
    recent = prices[-10:]  # ۱۰ روز اخیر
    avg = sum(recent) / len(recent)
    
    # روند ساده
    trend = (prices[-1] - prices[-5]) / 5
    
    predictions = []
    last_price = prices[-1]
    for i in range(1, days_ahead + 1):
        pred = last_price + (trend * i)
        # کمی به سمت میانگین برگرد
        pred = pred * 0.7 + avg * 0.3
        predictions.append(pred)
    return predictions

def main():
    coin = input("اسم ارز رو وارد کن (مثلاً bitcoin یا ethereum): ").strip().lower()
    if not coin:
        coin = "bitcoin"
    
    print(f"\nدر حال دریافت داده برای {coin}...")
    try:
        prices = get_price_data(coin, days=30)
        current = prices[-1]
        print(f"قیمت فعلی: ${current:,.2f}")
        
        predictions = simple_predict(prices, days_ahead=7)
        
        print("\nپیش‌بینی ۷ روز آینده:")
        for i, price in enumerate(predictions, 1):
            change = ((price - current) / current) * 100
            sign = "+" if change >= 0 else ""
            print(f"  روز {i}: ${price:,.2f}  ({sign}{change:.2f}%)")
            
    except Exception as e:
        print("خطا در دریافت داده:", e)
        print("اینترنت یا فیلترشکن رو چک کن.")

if __name__ == "__main__":
    main()
