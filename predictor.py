import numpy as np
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense, Dropout
import matplotlib.pyplot as plt

class CryptoPredictor:
    def __init__(self, look_back=30):
        self.look_back = look_back
        self.scaler = MinMaxScaler(feature_range=(0, 1))
        self.model = None

    def prepare_data(self, df):
        data = df["price"].values.reshape(-1, 1)
        scaled = self.scaler.fit_transform(data)
        
        X, y = [], []
        for i in range(self.look_back, len(scaled)):
            X.append(scaled[i - self.look_back:i, 0])
            y.append(scaled[i, 0])
        
        X, y = np.array(X), np.array(y)
        X = np.reshape(X, (X.shape[0], X.shape[1], 1))
        return X, y

    def build_model(self):
        model = Sequential([
            LSTM(50, return_sequences=True, input_shape=(self.look_back, 1)),
            Dropout(0.2),
            LSTM(50, return_sequences=False),
            Dropout(0.2),
            Dense(25),
            Dense(1)
        ])
        model.compile(optimizer="adam", loss="mean_squared_error")
        self.model = model
        return model

    def train(self, X, y, epochs=20, batch_size=32):
        if self.model is None:
            self.build_model()
        self.model.fit(X, y, epochs=epochs, batch_size=batch_size, verbose=1)

    def predict_next_days(self, last_data, days=7):
        predictions = []
        current_batch = last_data[-self.look_back:].reshape(1, self.look_back, 1)
        
        for _ in range(days):
            pred = self.model.predict(current_batch, verbose=0)[0][0]
            predictions.append(pred)
            current_batch = np.append(current_batch[:, 1:, :], [[[pred]]], axis=1)
        
        predictions = self.scaler.inverse_transform(np.array(predictions).reshape(-1, 1))
        return predictions.flatten()

    def plot_results(self, df, predictions, days=7):
        last_date = df["date"].iloc[-1]
        future_dates = [last_date + pd.Timedelta(days=i+1) for i in range(days)]
        
        plt.figure(figsize=(12, 6))
        plt.plot(df["date"], df["price"], label="قیمت واقعی")
        plt.plot(future_dates, predictions, label="پیش‌بینی", linestyle="--", marker="o")
        plt.title("پیش‌بینی قیمت ارز دیجیتال")
        plt.xlabel("تاریخ")
        plt.ylabel("قیمت (USD)")
        plt.legend()
        plt.grid(True)
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.show()
