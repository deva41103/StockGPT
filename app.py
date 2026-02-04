from flask import Flask, request, jsonify
from predictor import predict_price
from stock_info import get_stock_details

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


# 💬 CHATBOT-LIKE API
@app.route("/chat", methods=["POST"])
def chat():
    text = request.json.get("message", "").lower()

    if "tomorrow" in text:
        horizon = "1d"
    elif "month" in text:
        horizon = "1m"
    elif "year" in text:
        horizon = "1y"
    else:
        horizon = "1d"

    words = text.split()
    symbol = next((w.upper() for w in words if w.endswith(".NS")), None)

    if not symbol:
        return {"error": "Stock symbol not found in message"}, 400

    return jsonify(predict_price(symbol, horizon))


if __name__ == "__main__":
    app.run(debug=True)
