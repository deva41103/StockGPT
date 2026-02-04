import yfinance as yf

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
