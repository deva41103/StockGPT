from flask import Flask, request, jsonify
from predictor import predict_price
from stock_info import get_stock_details
import re
from nlp_parser import parse_message
from stock_info import get_historical_price_series

app = Flask(__name__)

@app.route("/")
def home():
    return {"message": "StockGPT API is running 🚀"}


# 🔮 PRICE PREDICTION API
@app.route("/predict", methods=["GET"])
def predict():
    symbol = request.args.get("symbol")
    horizon = request.args.get("horizon", "1d")

    if not symbol:
        return {"error": "symbol is required"}, 400

    result = predict_price(symbol, horizon)
    return jsonify(result)


# 📊 STOCK DETAILS API
@app.route("/stock-info", methods=["GET"])
def stock_info():
    symbol = request.args.get("symbol")
    if not symbol:
        return {"error": "symbol is required"}, 400

    return jsonify(get_stock_details(symbol))


@app.route("/chat", methods=["POST"])
def chat():
    text = request.json.get("message", "")

    parsed = parse_message(text)

    if not parsed:
        return {"error": "Could not understand stock or request"}, 400

    # 📊 CHART REQUEST
    if parsed["intent"] == "chart":
        return jsonify(
            get_historical_price_series(
                parsed["symbol"],
                parsed["range_or_horizon"]
            )
        )

    # 🔮 PRICE PREDICTION
    return jsonify(
        predict_price(
            parsed["symbol"],
            parsed["range_or_horizon"]
        )
    )

# 📊 HISTORICAL PRICE CHART API
@app.route("/chart", methods=["GET"])
def chart():
    symbol = request.args.get("symbol")
    range = request.args.get("range", "1m")

    if not symbol:
        return {"error": "symbol is required"}, 400

    data = get_historical_price_series(symbol, range)

    if not data:
        return {"error": "No data found"}, 404

    return jsonify(data)


if __name__ == "__main__":
    app.run(debug=True)

