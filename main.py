from data_fetcher import get_historical_data, get_current_price
from predictor import CryptoPredictor
import argparse

def main():
    parser = argparse.ArgumentParser(description="پیش‌بینی قیمت ارز دیجیتال")
    parser.add_argument("--coin", default="bitcoin", help="شناسه ارز (مثلاً bitcoin, ethereum)")
    parser.add_argument("--days", type=int, default=90, help="تعداد روزهای داده تاریخی")
    parser.add_argument("--predict", type=int, default=7, help="تعداد روزهای پیش‌بینی")
    parser.add_argument("--epochs", type=int, default=15, help="تعداد epoch آموزش")
    args = parser.parse_args()

    print(f"در حال دریافت داده برای {args.coin}...")
    df = get_historical_data(coin_id=args.coin, days=args.days)
    current = get_current_price(coin_id=args.coin)
    print(f"قیمت فعلی: ${current:,.2f}")

    predictor = CryptoPredictor(look_back=30)
    X, y = predictor.prepare_data(df)
    
    print("در حال آموزش مدل...")
    predictor.train(X, y, epochs=args.epochs)

    last_scaled = predictor.scaler.transform(df["price"].values.reshape(-1, 1))
    predictions = predictor.predict_next_days(last_scaled, days=args.predict)

    print("\nپیش‌بینی قیمت برای روزهای آینده:")
    for i, price in enumerate(predictions, 1):
        print(f"  روز {i}: ${price:,.2f}")

    predictor.plot_results(df, predictions, days=args.predict)

if __name__ == "__main__":
    main()
