# Developer Documentation for StockGPT

## 📌 Project Overview
**StockGPT** is an AI-driven, NLP-powered stock market prediction and analysis backend. Unlike the previous documentation which incorrectly mentioned React and Express, this project is built entirely in **Python** using the **Flask** microframework. 

The application is specifically designed to analyze and predict price movements for **NIFTY 50** stocks. It utilizes pre-trained LSTM (Long Short-Term Memory) machine learning models on historical market data (via `yfinance`) and technical indicators (RSI, MACD) to forecast future trends. Additionally, it offers a chatbot-like natural language parsing endpoint to interpret user intent (e.g., "show me the chart for Reliance" vs. "predict TCS for next month").

---

## 🏗️ Architecture & Technology Stack

The system follows a modular monolithic architecture centered around a Flask application that serves JSON API endpoints.

**Core Technologies**:
- **Backend**: Python 3, Flask
- **Data Acquisition**: `yfinance` (for historical and live market data)
- **Data Manipulation**: `pandas`, `numpy`
- **Machine Learning**: `tensorflow` / `keras` (LSTM models), `scikit-learn` & `joblib` (for data scaling)
- **Technical Analysis**: `ta` (Technical Analysis Library in Python)
- **NLP**: Basic Regular Expressions (`re`) for intent and entity extraction

---

## ⚙️ How it Works & Workflow

1. **User Request**: A client (e.g., frontend app, mobile app) sends an HTTP request to one of the Flask endpoints.
2. **Natural Language Parsing**: If requested via the `/chat` endpoint, the message is parsed using `nlp_parser.py` to determine the user's intent (charting vs. prediction), time horizon (e.g., 1 day, 1 week, 1 month), and the designated NIFTY 50 stock.
3. **Data Fetching & Preprocessing**: For predictions, `predictor.py` retrieves the last 2 years of daily stock prices. It calculates standard technical indicators (14-day RSI, MACD, and MACD Signal values) and shapes the data back 60 days to match the input shape of the trained LSTM model.
4. **Model Inference**: 
   - Uses pre-trained `lstm_sentiment.h5` models stored per-stock inside the `models/` directory.
   - Autoregressively predicts future prices for the requested timeline (1 day, 30 days, 252 days).
5. **Response Generation**: The results (Stock info, Historical Series, or Future Predictions) are formatted as JSON and returned to the client.

---

## 📂 Folder and File Structure

```text
/StockGPT
  ├── app.py                  # The main Flask application and API route definitions, also serves the UI.
  ├── predictor.py            # Core ML prediction logic (Loads models, standardizes data, runs inference).
  ├── stock_info.py           # Uses yfinance to fetch live details and historical charts.
  ├── nlp_parser.py           # Extracts user intent, time horizons, and stock symbols from text.
  ├── stocks.py               # Dictionary mapping common stock names to Yahoo Finance NIFTY 50 tickers (.NS).
  ├── static/                 # Contains CSS and JS files for the frontend web interface.
  ├── templates/              # Contains the HTML template (index.html) for the web interface.
  ├── models/                 # Stores pre-trained TensorFlow models (lstm_sentiment.h5) & scalers (scaler.pkl).
  ├── requirements.txt        # PIP dependencies list.
  ├── StockGpt.ipynb          # Jupyter Notebooks for data exploration and LSTM model training.
  ├── StockGptMl.ipynb        # Additional ML experimentations and training pipelines.
  └── developers.md           # This document!
```

### Detailed File Breakdown
- **`app.py`**: The entry point. Initializes the Flask server, wires up REST APIs (`/predict`, `/stock-info`, `/chat`, `/chart`), and serves the main web interface (`/`).
- **`predictor.py`**: The heavy lifter. Contains `predict_price()`. It loads the specific LSTM model for a stock, calculates indicators using the `ta` library, runs standard scaling on the features `[Close, Volume, RSI, MACD, MACD_signal, Sentiment]`, makes sequential predictions using a sliding window approach of sizes up to `LOOKBACK = 60`, and un-scales the results to return expected closing prices.
- **`stock_info.py`**: Exposes utility functions (`get_stock_details` and `get_historical_price_series`) strictly for fetching market metadata.
- **`nlp_parser.py`**: A rule-engine NLP mechanism. Scans words for synonyms of "chart" or "predict", looks for temporal words ("week", "tomorrow"), and matches strings to valid keys via the `stocks` mapping.
- **`stocks.py`**: A hardcoded lookup table mapping NIFTY 50 entities (e.g., "INFY", "TCS", "HDFC") to their corresponding NSE suffix tags expected by Yahoo Finance (`INFY.NS`, `TCS.NS`, `HDFCBANK.NS`).
- **`static/` & `templates/`**: These directories contain the frontend assets (HTML, CSS, JS) that compose the StockGPT web interface, allowing users to interact with NLP endpoints via a chat-like format.
- **`models/`**: The artifact repository containing subfolders for each ticker symbol containing the `.h5` model weights and `.pkl` object for the Scikit-learn normalizers.

---

## 🔌 API Endpoints

- **`GET /`**
  - **Description**: Serves the main web interface (`index.html`).
  - **Returns**: HTML content for the frontend.

- **`GET /predict`**
  - **Params**: `symbol` (e.g., INFY.NS), `horizon` (1d, 1m, 1y).
  - **Description**: Returns ML-generated price predictions.

- **`GET /stock-info`**
  - **Params**: `symbol`
  - **Description**: Fetches the company's market cap, sector, pricing highs/lows, and current quote.

- **`GET /chart`**
  - **Params**: `symbol`, `range` (1m, 3m, 6m, 1y).
  - **Description**: Returns historical timeseries closing prices formatted for UI charts.

- **`POST /chat`**
  - **Payload Structure**: `{"message": "Will TCS go up tomorrow?"}`
  - **Description**: The cornerstone endpoint. Parsers intent to serve either a historical chart or an ML prediction automatically based on English commands.

---

## 🛠 Setup & Development Guidelines

1. **Environment Setup**:
   Create a Python virtual environment and install dependencies:
   ```bash
   python -m venv env
   source env/bin/activate  # Or `env\Scripts\activate` on Windows
   pip install -r requirements.txt
   ```
2. **Running the Server**:
   ```bash
   python app.py
   ```
   The API will be available at `http://localhost:5000`.

3. **Modifying the Model**:
   If you wish to re-train models, use the `StockGptMl.ipynb` and `StockGpt.ipynb` notebooks. Once training completes, overwrite the files situated within `models/{ticker}/`. Keep track of the feature matrix size, especially dummy placeholders exactly like `Sentiment` (which currently defaults to 0.0) as they must match the input size of the LSTM layers.`