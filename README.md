# AI-Powered Business Intelligence and Predictive Analytics System

A Flask-based academic portfolio project that demonstrates how business data can be converted into descriptive insights, baseline predictions, anomaly flags and practical data-quality recommendations.

## Features
- Upload and analyze CSV business datasets
- Dataset overview, missing-value and duplicate checks
- Numeric metric summary and interactive trend chart
- Random Forest regression baseline with MAE, RMSE and R²
- Isolation Forest anomaly detection
- Rule-based recommendations
- Downloadable sample dataset

## Requirements
- Python 3.10 or newer
- Windows, macOS or Linux
- Internet connection for the Chart.js CDN used by the dashboard

## Windows setup
1. Install Python 3.10+ and select **Add Python to PATH** during installation.
2. Extract this ZIP file.
3. Open the extracted project folder.
4. In File Explorer, click the address bar, type `cmd`, and press Enter.
5. Create a virtual environment:
   `python -m venv .venv`
6. Activate it:
   `.venv\Scripts\activate`
7. Install dependencies:
   `python -m pip install -r requirements.txt`
8. Start the application:
   `python app.py`
9. Open `http://127.0.0.1:5000` in your browser.

## macOS / Linux setup
1. Open Terminal in the extracted project folder.
2. Create a virtual environment:
   `python3 -m venv .venv`
3. Activate it:
   `source .venv/bin/activate`
4. Install dependencies:
   `python -m pip install -r requirements.txt`
5. Start the application:
   `python app.py`
6. Open `http://127.0.0.1:5000` in your browser.

## Use your own data
Upload a CSV file from the dashboard. The app automatically identifies numeric columns and selects a target using common names such as `sales`, `revenue`, `profit`, `quantity`, `units`, `amount` or `orders`. If none match, it uses the first numeric column.

For meaningful predictive results, use at least 30 rows and include a numeric outcome column. If your data contains dates, sort the CSV chronologically before uploading. The current model is a demonstration baseline and does not yet implement time-series forecasting.

## Suggested CSV structure
`date,region,category,sales,marketing_spend,orders,profit`

A sample file is included at `data/demo_business_data.csv`.

## Project structure
```text
AI-Powered-Business-Intelligence-System/
├── app.py
├── requirements.txt
├── README.md
├── src/
│   ├── __init__.py
│   └── analytics.py
├── templates/
│   └── index.html
├── static/
│   └── style.css
└── data/
    └── demo_business_data.csv
```

## Important limitations
- This is an educational portfolio prototype, not a production decision system.
- Predictions are baseline estimates; validate them on suitable real-world data.
- Isolation Forest flags unusual records, not confirmed fraud or errors.
- Recommendations are rule-based and should be reviewed by a domain expert.
- Uploaded files are stored locally in `data/uploads/`. Do not upload confidential or personal data.
- Before public deployment, configure a secure secret key, disable debug mode, add authentication, validate schemas and use secure storage.

## GitHub publishing checklist
1. Create a new public repository named `AI-Powered-Business-Intelligence-System`.
2. Add the extracted project files.
3. Do not upload `.venv`, private datasets, credentials or confidential files.
4. Add a clear repository description and topics such as `python`, `flask`, `machine-learning`, `business-analytics`, `predictive-analytics`.
5. Include dashboard screenshots in a `screenshots/` folder after running the app.
6. Commit and push the project.
