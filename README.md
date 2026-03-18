# StockGPT

StockGPT is an AI-driven, NLP-powered stock market prediction and analysis platform specifically designed for NIFTY 50 stocks. It provides both a robust backend API and a built-in web-based chat interface to interact with the system using natural language.

## Key Features

- **Price Prediction**: Forecasts stock prices based on historical data using pre-trained LSTM machine learning models.
- **Natural Language Chat**: Understands user queries like "show me the chart for Reliance" or "predict TCS for next month" using a built-in NLP parser.
- **Stock Information & Charts**: Fetches current stock details, quotes, and historical time-series data via Yahoo Finance.
- **Interactive Web UI**: A frontend application that allows users to seamlessly retrieve charts, predictions, and stock information.

## Quick Start

1. **Clone the repository and set up a Virtual Environment**:
   ```bash
   python -m venv env
   # On macOS/Linux:
   source env/bin/activate
   # On Windows:
   env\Scripts\activate
   ```

2. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the Application**:
   ```bash
   python app.py
   ```

4. **Access the Interface**:
   Open a web browser and go to `http://localhost:5000` to start chatting with the AI.

## Further Reading

For an in-depth explanation of the project setup, ML model integration, NLP logic, folder structures, and direct API endpoints, please read [Developer Documentation (developers.md)](developers.md).
