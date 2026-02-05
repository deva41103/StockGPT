import yfinance as yf
import pandas as pd

def get_stock_details(symbol):
    stock = yf.Ticker(symbol)
    info = stock.info

    return {
        "symbol": symbol,
        "name": info.get("shortName"),
        "sector": info.get("sector"),
        "market_cap": info.get("marketCap"),
        "52_week_high": info.get("fiftyTwoWeekHigh"),
        "52_week_low": info.get("fiftyTwoWeekLow"),
        "current_price": info.get("currentPrice")
    }

def get_historical_price_series(symbol, range="1m"):
    range_map = {
        "1w": "7d",
        "1m": "1mo",
        "3m": "3mo",
        "6m": "6mo",
        "1y": "1y"
    }

    period = range_map.get(range, "1mo")

    df = yf.download(
        symbol,
        period=period,
        auto_adjust=False,
        progress=False
    )

    if df.empty:
        return None

    # Handle MultiIndex safely
    if isinstance(df.columns, pd.MultiIndex):
        df.columns = df.columns.get_level_values(0)

    series = []
    for date, row in df.iterrows():
        series.append({
            "date": date.strftime("%Y-%m-%d"),
            "price": round(float(row["Close"]), 2)
        })

    return {
        "symbol": symbol,
        "range": range,
        "series": series
    }