import re
from stocks import NIFTY_STOCKS

def parse_message(text: str):
    text = text.lower()

    # -------- INTENT --------
    if any(w in text for w in ["chart", "graph", "plot", "history"]):
        intent = "chart"
    else:
        intent = "predict"

    # -------- RANGE / HORIZON --------
    if "week" in text:
        range_or_horizon = "1w"
    elif "month" in text:
        range_or_horizon = "1m"
    elif "year" in text:
        range_or_horizon = "1y"
    elif "tomorrow" in text or "day" in text:
        range_or_horizon = "1d"
    else:
        range_or_horizon = "1m" if intent == "chart" else "1d"

    # -------- STOCK --------
    words = re.findall(r"[a-zA-Z]+", text)
    for w in words:
        key = w.upper()
        if key in NIFTY_STOCKS:
            return {
                "intent": intent,
                "symbol": NIFTY_STOCKS[key],
                "range_or_horizon": range_or_horizon
            }

    return None
