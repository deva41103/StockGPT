import numpy as np
import pandas as pd
import joblib
import yfinance as yf
import ta
from tensorflow.keras.models import load_model
from tensorflow.keras.losses import MeanSquaredError

LOOKBACK = 60
BASE_DIR = "models"


# ---------------- LOAD MODEL ----------------
def load_stock_model(symbol):
    model = load_model(
        f"{BASE_DIR}/{symbol}/lstm_sentiment.h5",
        custom_objects={"mse": MeanSquaredError()}
    )
    scaler = joblib.load(f"{BASE_DIR}/{symbol}/scaler.pkl")
    return model, scaler


# ---------------- PREPARE DATA ----------------
def prepare_data(symbol):
    df = yf.download(symbol, period="2y", auto_adjust=False)

    # 🔑 Flatten yfinance MultiIndex safely
    df = df[['Close', 'Volume']]
    df.columns = ['Close', 'Volume']

    # ✅ MUST be pandas Series
    close = pd.Series(df['Close'].values, index=df.index)

    df['RSI'] = ta.momentum.RSIIndicator(close=close, window=14).rsi()

    macd = ta.trend.MACD(close=close)
    df['MACD'] = macd.macd()
    df['MACD_signal'] = macd.macd_signal()

    # ✅ DUMMY SENTIMENT (model was trained with it)
    df['Sentiment'] = 0.0

    df.dropna(inplace=True)
    return df


# ---------------- PREDICTION ----------------
def predict_price(symbol, horizon="1d"):
    model, scaler = load_stock_model(symbol)
    df = prepare_data(symbol)

    features = [
        'Close',
        'Volume',
        'RSI',
        'MACD',
        'MACD_signal',
        'Sentiment'
    ]

    scaled = scaler.transform(df[features])

    window = scaled[-LOOKBACK:].reshape(1, LOOKBACK, scaled.shape[1])

    steps = {"1d": 1, "1m": 30, "1y": 252}.get(horizon, 1)

    preds = []
    temp = window.copy()

    for _ in range(steps):
        p = float(model(temp, training=False).numpy()[0][0])
        preds.append(p)

        next_row = temp[0, -1].copy()
        next_row[0] = p
        temp = np.roll(temp, -1, axis=1)
        temp[0, -1] = next_row

    mean_scaled = float(np.mean(preds))

    dummy = np.zeros((1, scaled.shape[1]))
    dummy[0, 0] = mean_scaled
    price = float(scaler.inverse_transform(dummy)[0, 0])

    # ✅ FIXED: extract scalar safely
    last_close = float(df['Close'].iloc[-1])

    return {
        "symbol": symbol,
        "horizon": horizon,
        "last_close": round(last_close, 2),
        "expected_price": round(price, 2),
        "direction": "UP" if price > last_close else "DOWN"
    }
