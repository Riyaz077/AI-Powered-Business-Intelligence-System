import os
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestRegressor, IsolationForest
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

NUMERIC_CANDIDATES = ["sales", "revenue", "profit", "quantity", "units", "amount", "orders"]

def generate_demo_data(path="data/demo_business_data.csv", n=240, seed=42):
    rng = np.random.default_rng(seed)
    dates = pd.date_range("2025-01-01", periods=n, freq="D")
    trend = np.linspace(900, 1500, n)
    season = 150 * np.sin(np.arange(n) * 2 * np.pi / 7)
    sales = trend + season + rng.normal(0, 90, n)
    sales[[55, 145, 201]] *= [2.1, 0.35, 2.4]
    marketing = rng.uniform(80, 350, n)
    orders = np.maximum(10, (sales / rng.uniform(25, 45, n)).astype(int))
    cost = sales * rng.uniform(0.55, 0.78, n)
    df = pd.DataFrame({
        "date": dates.strftime("%Y-%m-%d"),
        "region": rng.choice(["North", "South", "East", "West"], n),
        "category": rng.choice(["Electronics", "Home", "Fashion", "Grocery"], n),
        "sales": np.round(sales, 2),
        "marketing_spend": np.round(marketing, 2),
        "orders": orders,
        "profit": np.round(sales - cost - marketing, 2)
    })
    os.makedirs(os.path.dirname(path), exist_ok=True)
    df.to_csv(path, index=False)
    return df

def load_dataset(path):
    df = pd.read_csv(path)
    if df.empty:
        raise ValueError("The CSV file has no rows.")
    if len(df.columns) < 2:
        raise ValueError("The CSV should contain at least two columns.")
    return df

def _find_numeric_target(df):
    lower_map = {c.lower(): c for c in df.columns}
    for name in NUMERIC_CANDIDATES:
        if name in lower_map and pd.api.types.is_numeric_dtype(df[lower_map[name]]):
            return lower_map[name]
    numeric = df.select_dtypes(include=np.number).columns.tolist()
    return numeric[0] if numeric else None

def analyze_dataset(df):
    clean = df.copy()
    numeric_cols = clean.select_dtypes(include=np.number).columns.tolist()
    target = _find_numeric_target(clean)

    # Coerce date-like columns for reporting only; retain original data for modelling.
    date_cols = [c for c in clean.columns if "date" in c.lower() or "time" in c.lower()]
    date_label = date_cols[0] if date_cols else None

    total_rows = len(clean)
    missing_total = int(clean.isna().sum().sum())
    duplicate_rows = int(clean.duplicated().sum())
    total_value = float(clean[target].fillna(0).sum()) if target else 0.0
    average_value = float(clean[target].mean()) if target else 0.0

    summary = clean.describe(include="all").fillna("").to_dict()
    summary_rows = []
    for col in clean.columns:
        summary_rows.append({
            "column": col,
            "type": str(clean[col].dtype),
            "missing": int(clean[col].isna().sum()),
            "unique": int(clean[col].nunique(dropna=True))
        })

    chart_labels, chart_values = [], []
    if target:
        grouped = clean[target].dropna().head(30)
        chart_labels = [str(i + 1) for i in range(len(grouped))]
        chart_values = [round(float(v), 2) for v in grouped.tolist()]

    category_insights = []
    categorical = clean.select_dtypes(exclude=np.number).columns.tolist()
    for col in categorical[:2]:
        counts = clean[col].fillna("Missing").astype(str).value_counts().head(6)
        category_insights.append({"column": col, "items": [{"name": str(k), "count": int(v)} for k, v in counts.items()]})

    anomalies = []
    model_metrics = None
    forecast = []
    if numeric_cols:
        X = clean[numeric_cols].replace([np.inf, -np.inf], np.nan)
        X = X.fillna(X.median(numeric_only=True)).fillna(0)
        if len(X) >= 20:
            detector = IsolationForest(contamination=0.05, random_state=42)
            labels = detector.fit_predict(X)
            anomaly_indices = np.where(labels == -1)[0][:10]
            for idx in anomaly_indices:
                anomalies.append({"row": int(idx + 1), "value": round(float(clean.iloc[idx][target]), 2) if target else "N/A"})
        if target and len(numeric_cols) >= 1 and len(clean) >= 30:
            features = [c for c in numeric_cols if c != target]
            if not features:
                # Use row order as a simple trend feature when only one numeric field exists.
                X_model = pd.DataFrame({"row_number": np.arange(len(clean))})
            else:
                X_model = clean[features].copy()
            y = clean[target].copy()
            valid = y.notna()
            X_model, y = X_model.loc[valid], y.loc[valid]
            if len(y) >= 30:
                split = max(1, int(len(y) * 0.8))
                X_train, X_test = X_model.iloc[:split], X_model.iloc[split:]
                y_train, y_test = y.iloc[:split], y.iloc[split:]
                if len(X_test) > 0:
                    pipe = Pipeline([("imputer", SimpleImputer(strategy="median")), ("model", RandomForestRegressor(n_estimators=120, random_state=42))])
                    pipe.fit(X_train, y_train)
                    pred = pipe.predict(X_test)
                    model_metrics = {
                        "mae": round(float(mean_absolute_error(y_test, pred)), 2),
                        "rmse": round(float(np.sqrt(mean_squared_error(y_test, pred))), 2),
                        "r2": round(float(r2_score(y_test, pred)), 3) if len(y_test) > 1 else None
                    }
                    recent = X_model.tail(1).copy()
                    forecast = [round(float(v), 2) for v in pipe.predict(pd.concat([recent] * 7, ignore_index=True))]

    recommendations = []
    if missing_total:
        recommendations.append(f"Review {missing_total} missing values before using the dataset for operational decisions.")
    if duplicate_rows:
        recommendations.append(f"Investigate {duplicate_rows} duplicate records and remove confirmed duplicates.")
    if anomalies:
        recommendations.append(f"Review the {len(anomalies)} unusual records flagged by Isolation Forest; anomalies are not automatically errors.")
    if target and average_value:
        recommendations.append(f"Track {target} regularly against its average ({average_value:,.2f}) and investigate sustained deviations.")
    if not recommendations:
        recommendations.append("The dataset passed basic quality checks. Continue monitoring key metrics and refresh the analysis with new data.")

    return {
        "total_rows": total_rows,
        "total_columns": len(clean.columns),
        "missing_total": missing_total,
        "duplicate_rows": duplicate_rows,
        "target": target or "No numeric target found",
        "total_value": round(total_value, 2),
        "average_value": round(average_value, 2),
        "summary_rows": summary_rows,
        "chart_labels": chart_labels,
        "chart_values": chart_values,
        "category_insights": category_insights,
        "anomalies": anomalies,
        "metrics": model_metrics,
        "forecast": forecast,
        "recommendations": recommendations
    }
