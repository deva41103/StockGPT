# StockGPT Developer Documentation

## Project Overview
StockGPT is a stock prediction application that utilizes machine learning algorithms to predict stock prices based on historical data.

## Architecture
The application follows a modular architecture, separating different functionalities into distinct components:
- **Data Collection**: Responsible for gathering historical stock data.
- **Data Processing**: Processes and cleans the data for analysis.
- **Machine Learning Model**: Implements various algorithms for prediction.
- **API Layer**: Exposes endpoints for user interaction and predictions.

## File Structure
```
StockGPT/
├── data/
│   ├── collect.py           # Script for data collection
│   ├── process.py          # Script for data preprocessing
├── models/
│   ├── prediction_model.py  # Machine learning model implementation
├── api/
│   ├── app.py               # API endpoints
└── requirements.txt         # Project dependencies
```

## Code Flow
1. **Data Collection**: Trigger the `collect.py` script to gather stock data.
2. **Data Processing**: Run `process.py` to clean and prepare data for the model.
3. **Model Training**: Train the model using `prediction_model.py` on the cleaned dataset.
4. **API Queries**: Utilize the API endpoints defined in `app.py` to make predictions based on user inputs.

## API Endpoints
- **GET /api/predict**: Returns stock price predictions based on the given parameters.
- **POST /api/train**: Initiates model training on new data provided.

### Example Request
```json
{
  "ticker": "AAPL",
  "start_date": "2025-01-01",
  "end_date": "2025-12-31"
}
```
### Example Response
```json
{
  "predicted_price": 150.25,
  "confidence_interval": [145.00, 155.00]
}
```

## Conclusion
This documentation provides a high-level overview of the StockGPT application structure, functionality, and usage. For detailed code explanations, please refer to the source code within each module.