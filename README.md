# AI-Powered Business Intelligence and Predictive Analytics System

An interactive Streamlit-based business intelligence platform that transforms raw business datasets into meaningful insights through descriptive analytics, machine learning-based prediction, anomaly detection, and rule-based decision support.

The system enables users to upload business data, evaluate dataset quality, explore key performance indicators, estimate business outcomes, identify unusual observations, and generate practical recommendations through a centralized interactive dashboard.

<p align="center">

**Business Analytics · Machine Learning · Predictive Intelligence · Decision Support**

</p>

---

## Overview

Modern businesses generate large volumes of operational data, but converting that data into actionable decisions requires effective analytical tools.

This project demonstrates an integrated business intelligence workflow that combines data preprocessing, descriptive analytics, predictive modelling, anomaly detection, and recommendation generation within an interactive Streamlit web application.

Users can upload their own CSV datasets or explore the included sample dataset to understand business performance and discover potentially important patterns.

### Key Highlights

- **Data Analysis:** Upload and explore structured business datasets.
- **Data Quality Assessment:** Identify missing values, duplicate records, and dataset characteristics.
- **Business Intelligence:** Generate numerical summaries, performance indicators, and analytical insights.
- **Predictive Analytics:** Apply Random Forest Regression as a baseline predictive model.
- **Anomaly Detection:** Use Isolation Forest to identify unusual observations.
- **Decision Support:** Generate practical, rule-based business recommendations.
- **Interactive Dashboard:** Explore analytical results through a centralized Streamlit interface.

---

## System Architecture

The application follows a modular analytical architecture in which uploaded business data passes through preprocessing, analytics, machine learning, and recommendation components before the results are presented through the Streamlit dashboard.

### 1. Overall System Architecture

```mermaid
flowchart TB
    A["Business CSV Dataset"] --> B["Streamlit Web Application"]
    B --> C["Dataset Upload and Validation"]

    C --> D["Data Preprocessing"]
    D --> E["Data Quality Assessment"]

    E --> F["Descriptive Analytics"]
    E --> G["Predictive Analytics"]
    E --> H["Anomaly Detection"]

    F --> I["Business Metrics and Insights"]
    G --> J["Random Forest Regression"]
    H --> K["Isolation Forest"]

    I --> L["Analytical Results"]
    J --> L
    K --> L

    L --> M["Rule-Based Recommendation Engine"]
    M --> N["Interactive Business Intelligence Dashboard"]

    N --> O["Analytical Results and Visualizations"]
    N --> P["Downloadable Outputs"]
```

### 2. Core System Components

| Component | Technology / Method | Purpose |
|---|---|---|
| Web application | Streamlit | Handles dashboard navigation and user interaction |
| Data ingestion | Pandas | Reads and processes uploaded CSV files |
| Data validation | Pandas | Examines missing values, duplicates, and column structure |
| Descriptive analytics | Pandas, NumPy | Summarizes numerical metrics and business trends |
| Predictive modelling | Random Forest Regressor | Establishes a baseline for numerical outcome prediction |
| Anomaly detection | Isolation Forest | Identifies observations with unusual patterns |
| Recommendation engine | Rule-based logic | Converts analytical findings into practical suggestions |
| Dashboard visualization | Streamlit | Presents analytical results and dataset information |

### 3. End-to-End Analytical Workflow

```mermaid
flowchart TD
    A["Launch Streamlit Application"] --> B["Upload Business CSV"]
    B --> C["Validate Dataset"]
    C --> D["Inspect Data Structure"]

    D --> E["Check Missing Values and Duplicates"]
    E --> F["Identify Numeric Columns"]

    F --> G["Generate Descriptive Statistics"]
    G --> H["Calculate Business Metrics"]
    H --> I["Explore Analytical Results"]

    I --> J["Select Prediction Target"]
    J --> K["Train Random Forest Regression Baseline"]
    K --> L["Evaluate MAE, RMSE and R²"]

    L --> M["Apply Isolation Forest"]
    M --> N["Identify Anomalous Observations"]

    N --> O["Generate Rule-Based Recommendations"]
    O --> P["Display Results in Streamlit Dashboard"]
    P --> Q["Download Dataset"]
```

---

## Key Features

### 1. CSV Dataset Upload and Analysis

- Upload custom business datasets in CSV format.
- Read and process structured business records.
- Automatically identify numeric columns.
- Explore uploaded datasets through the dashboard.
- Display an overview of the uploaded dataset.

### 2. Data Quality Assessment

- Identify missing values across dataset columns.
- Detect duplicate records.
- Examine dataset dimensions and data types.
- Generate a basic data-quality profile.
- Highlight potential issues that may affect analytical reliability.

### 3. Descriptive Business Analytics

- Generate numerical summaries of business variables.
- Explore sales and other numeric business metrics.
- Analyze trends through descriptive analytics.
- Present important analytical information through dashboard outputs.

### 4. Random Forest Predictive Analytics

The application implements a Random Forest Regression baseline to demonstrate how machine learning can estimate a selected numerical business outcome.

**Evaluation metrics:**

| Metric | Purpose |
|---|---|
| MAE | Measures average absolute prediction error |
| RMSE | Measures prediction error while penalizing larger errors |
| R² Score | Measures the proportion of target variance explained by the model |

The model is intended for baseline experimentation rather than production-grade forecasting.

### 5. Isolation Forest Anomaly Detection

Isolation Forest is used to identify observations that differ significantly from the general data distribution.

Potential applications include:

- Unusual sales observations.
- Unexpected changes in business metrics.
- Uncommon transaction or operational patterns.
- Records requiring additional investigation.

An anomaly indicates an unusual observation, not necessarily an error, fraud, or business failure.

### 6. Rule-Based Business Recommendations

The application generates recommendations using analytical findings and predefined business rules.

Examples include:

- Reviewing unusual business metric variations.
- Investigating missing or duplicate records.
- Examining declining performance indicators.
- Reviewing unusual observations identified by anomaly detection.

These recommendations are generated through predefined logic rather than a trained generative AI model.

### 7. Interactive Streamlit Business Intelligence Dashboard

- Centralized dashboard for analytical results.
- Sidebar-based application navigation.
- Interactive CSV dataset upload.
- Demo dataset generation and analysis.
- Dataset overview and KPI presentation.
- Predictive model evaluation results.
- Anomaly detection outputs.
- Decision-support recommendations.
- Downloadable dataset outputs.

---

## Dashboard Screenshots

The following screenshots demonstrate the application interface and its analytical capabilities, from the initial dashboard experience to advanced analytical outputs and decision-support recommendations.

### 01. Dashboard Overview

The main Streamlit application interface, introducing the business intelligence platform and its analytical capabilities.

![Dashboard Overview](https://github.com/user-attachments/assets/12cb80df-b156-4092-8f4f-49d9dd880b28)

### 02. Business Analytics KPI Overview

A consolidated view of important business performance indicators and key analytical metrics.

![Business Analytics KPI Overview](https://github.com/user-attachments/assets/2804da56-bcbc-4ab0-9bbc-7ae9344b327a)

### 03. Business Data Quality Profile

An overview of dataset structure, missing values, duplicate records, and data-quality characteristics.

![Business Data Quality Profile](https://github.com/user-attachments/assets/de2e5d47-95a6-42c9-b410-b26ce6408eb7)

### 04. Descriptive Sales Analytics

Visual exploration of business metrics and sales patterns through descriptive analytics.

![Descriptive Sales Analytics](https://github.com/user-attachments/assets/e1269373-ff7a-4832-9a49-a75ccdcfba1d)

### 05. Business Performance Snapshot

A summarized view of business performance and important analytical observations.

<p align="center">
  <img src="https://github.com/user-attachments/assets/11a85fcb-4da3-4c7d-b00e-70155d8121b7" alt="Business Performance Snapshot" width="700">
</p>

### 06. Random Forest Predictive Analytics

Model-based business outcome estimation with regression evaluation metrics.

<p align="center">
  <img src="https://github.com/user-attachments/assets/96d1c95b-55b9-487f-81d7-1417bb906a33" alt="Random Forest Predictive Analytics" width="700">
</p>

### 07. Isolation Forest Anomaly Detection

Identification and visualization of unusual observations using unsupervised machine learning.

<p align="center">
  <img src="https://github.com/user-attachments/assets/349e8866-2a57-4965-8bf9-f51998024d25" alt="Isolation Forest Anomaly Detection" width="700">
</p>

### 08. Decision Intelligence Recommendations

Rule-based recommendations that translate analytical findings into practical business actions.

![Decision Intelligence Recommendations](https://github.com/user-attachments/assets/48dbc407-762c-4b24-9667-33415c1be497)

---

## Technology Stack

| Category | Technologies |
|---|---|
| Programming Language | Python |
| Web Application Framework | Streamlit |
| Data Processing | Pandas, NumPy |
| Machine Learning | Scikit-learn |
| Predictive Model | Random Forest Regression |
| Anomaly Detection | Isolation Forest |
| Dashboard Interface | Streamlit |
| Data Visualization | Streamlit charts and visual components |
| Dataset Format | CSV |
| Development Environment | VS Code, Python Virtual Environment |
| Cloud Deployment | Streamlit Community Cloud |

---

## Dataset

The application supports custom CSV datasets containing structured business information.

### Suggested Dataset Structure

```csv
date,region,category,sales,marketing_spend,orders,profit
2026-01-01,North,Electronics,12500,1500,85,3200
2026-01-02,South,Clothing,9800,1200,67,2400
2026-01-03,East,Furniture,15600,1800,92,4100
```

A sample dataset is included in:

`data/demo_business_data.csv`

### Automatic Target Selection

The application attempts to identify a numeric prediction target using common column names such as:

- `sales`
- `revenue`
- `profit`
- `quantity`
- `units`
- `amount`
- `orders`

If none of these names match, the first available numeric column is selected.

For meaningful baseline experimentation, use at least 30 records and include a numeric outcome column. Larger, representative datasets are preferable.

**Important:** Automatic target selection is a convenience, not a guarantee that the selected variable is the correct business prediction target. Review the selected target and available features before interpreting results.

For datasets containing dates, arrange records chronologically before upload. The current model does not implement dedicated time-series forecasting.

---

## Project Structure

```text
AI-Powered-Business-Intelligence-System/
│
├── app.py
├── requirements.txt
├── README.md
│
├── src/
│   ├── __init__.py
│   └── analytics.py
│
└── data/
    ├── demo_business_data.csv
    └── uploads/
```

### Directory Description

| File / Directory | Description |
|---|---|
| `app.py` | Main Streamlit application and dashboard entry point |
| `requirements.txt` | Python project dependencies |
| `src/analytics.py` | Analytical and machine learning functionality |
| `src/__init__.py` | Python package initialization |
| `data/` | Sample business dataset and uploaded data |
| `data/uploads/` | Directory for uploaded CSV files |
| `README.md` | Project documentation |

The previous Flask-specific `templates/` and `static/` folders are no longer required by the Streamlit interface.

---

## Installation and Setup

### Prerequisites

- Python 3.10 or newer
- Windows, macOS, or Linux
- Internet connection for installing Python dependencies

### Windows Installation

**Step 1: Clone the repository**

```bash
git clone https://github.com/Riyaz077/ai-powered-business-intelligence-system.git
```

**Step 2: Navigate to the project directory**

```bash
cd ai-powered-business-intelligence-system
```

**Step 3: Create a virtual environment**

```bash
python -m venv .venv
```

**Step 4: Activate the environment**

```bash
.venv\Scripts\activate
```

**Step 5: Install dependencies**

```bash
python -m pip install -r requirements.txt
```

**Step 6: Run the Streamlit application**

```bash
streamlit run app.py
```

**Step 7: Open the dashboard**

Navigate to:

```text
http://localhost:8501
```

The Streamlit application should now be accessible through your local browser.

### macOS / Linux

```bash
git clone https://github.com/Riyaz077/ai-powered-business-intelligence-system.git

cd ai-powered-business-intelligence-system

python3 -m venv .venv

source .venv/bin/activate

python -m pip install -r requirements.txt

streamlit run app.py
```

Then open `http://localhost:8501` in your browser.

---

## How to Use

1. Launch the Streamlit application.
2. Open the dashboard in your browser.
3. Navigate to the Dashboard section.
4. Generate and analyze the included demo business dataset.
5. Navigate to Upload Dataset to upload a custom CSV file.
6. Select Analyze Dataset to process the uploaded data.
7. Review the dataset overview and data-quality information.
8. Explore the analytical results and business metrics.
9. Examine the Random Forest regression results.
10. Review unusual observations identified by Isolation Forest.
11. Analyze the rule-based business recommendations.
12. Download the available dataset outputs.

---

## Model Evaluation

The application uses regression metrics to evaluate the Random Forest baseline.

| Metric | Interpretation |
|---|---|
| Mean Absolute Error (MAE) | Average magnitude of prediction errors |
| Root Mean Squared Error (RMSE) | Error measure that gives greater weight to large prediction errors |
| R² Score | Indicates how well the model explains variation in the target |

Model performance depends on dataset size, feature quality, target selection, train-test separation, and the underlying business patterns.

A high R² score alone does not establish that a model will generalize to future business conditions.

---

## Responsible Use and Ethical Considerations

1. **Data Privacy and Confidentiality:** Avoid uploading sensitive personal information, confidential business records, or datasets without authorization.

2. **Responsible AI Decision-Making:** Treat model predictions and recommendations as decision-support information requiring human validation.

3. **Model Transparency and Accountability:** Communicate model assumptions, evaluation metrics, limitations, and possible biases.

4. **Data Accuracy and Integrity:** Validate uploaded datasets and investigate missing, duplicate, and unusual records.

5. **Ethical and Fair AI Practices:** Avoid discriminatory or harmful applications of analytical outputs.

6. **Human Oversight:** Do not use anomaly flags or model predictions as the sole basis for important business decisions.

---

## Limitations

- Predictive results depend on the quality, size, and structure of uploaded datasets.
- The Random Forest implementation is a baseline regression model, not a dedicated time-series forecasting system.
- The current target-selection mechanism uses common column names and a numeric-column fallback.
- Isolation Forest identifies unusual observations but cannot independently determine their causes.
- Recommendations use predefined rules rather than a trained generative AI model.
- Uploaded datasets currently use local file storage.
- Authentication, role-based access control, and production-grade security are not implemented.
- Streamlit Community Cloud storage is not intended for persistent user-uploaded files.
- The application has not been presented as a production-validated enterprise BI solution.

---

## Future Enhancements

| Area | Planned Enhancement |
|---|---|
| Predictive Analytics | Advanced forecasting using XGBoost and LSTM |
| Business Intelligence | Expanded KPI monitoring and interactive filtering |
| Data Management | MySQL or PostgreSQL integration |
| Security | Authentication and role-based user management |
| Explainable AI | SHAP-based model interpretation |
| Reporting | Automated PDF business report generation |
| Real-Time Analytics | Streaming data processing and intelligent alerts |
| Deployment | Cloud hosting and scalable storage |
| Decision Support | Context-aware recommendations and configurable business rules |

---

## Deployment

The application is deployed using Streamlit Community Cloud, providing public access to the interactive business intelligence dashboard.

**Live Demo:** `https://intellix.streamlit.app/`

**Deployment Platform:** Streamlit Community Cloud

### Deployment Configuration

| Setting | Configuration |
|---|---|
| Repository | `Riyaz077/ai-powered-business-intelligence-system` |
| Branch | `main` |
| Main File | `app.py` |
| Framework | Streamlit |
| Dependency File | `requirements.txt` |

### Deployment Process

1. Push the project source code to GitHub.
2. Sign in to Streamlit Community Cloud using GitHub.
3. Create or configure the application using the project repository.
4. Select the `main` branch.
5. Set the main file path to `app.py`.
6. Deploy the application.
7. Access the dashboard through its public Streamlit URL.

The application runs directly through Streamlit without requiring a separate Flask server or Gunicorn process.

For production-oriented use, configure appropriate file handling, authentication, privacy controls, and persistent storage.

---

## License

This project is available for educational and portfolio demonstration purposes. No formal open-source license has been specified. A suitable license can be added separately if the project is distributed under defined open-source terms.

---

## Author

**Mohamed Riyaz S.**  
Integrated M.Tech – Computer Science and Engineering (Business Analytics)  
Vellore Institute of Technology (VIT), Chennai

Designed and developed as part of my technical portfolio, integrating web application development, business analytics, data processing, machine learning, and predictive decision-support techniques.

**Areas Demonstrated:** Python · Streamlit · Business Intelligence · Machine Learning · Predictive Analytics · Anomaly Detection · Data Visualization
