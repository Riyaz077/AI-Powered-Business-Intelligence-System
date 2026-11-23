from __future__ import annotations
import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import IsolationForest, RandomForestRegressor
from sklearn.impute import SimpleImputer
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder

def profile_dataset(df: pd.DataFrame) -> dict:
    cells = int(df.isna().sum().sum())
    total = max(int(df.shape[0] * df.shape[1]), 1)
    duplicates = int(df.duplicated().sum())
    rows = max(len(df), 1)
    return {
        "missing_cells": cells,
        "missing_pct": cells / total * 100,
        "duplicates": duplicates,
        "duplicate_pct": duplicates / rows * 100,
    }

def prepare_regression(df, target, test_size=0.2):
    data = df.copy()
    data[target] = pd.to_numeric(data[target], errors="coerce")
    data = data.dropna(subset=[target])
    if len(data) < 10:
        raise ValueError("At least 10 usable rows are recommended for a train/test evaluation.")
    y = data[target]
    X = data.drop(columns=[target])
    # Remove columns with no information and high-cardinality free text / identifiers.
    X = X.loc[:, X.nunique(dropna=True) > 1]
    if X.empty:
        raise ValueError("No usable feature columns remain after excluding the target.")
    numeric = X.select_dtypes(include=np.number).columns.tolist()
    categorical = X.select_dtypes(exclude=np.number).columns.tolist()
    transformers = []
    if numeric:
        transformers.append(("numeric", SimpleImputer(strategy="median"), numeric))
    if categorical:
        transformers.append(("categorical", Pipeline([
            ("imputer", SimpleImputer(strategy="most_frequent")),
            ("encoder", OneHotEncoder(handle_unknown="ignore", sparse_output=False))
        ]), categorical))
    pre = ColumnTransformer(transformers, remainder="drop")
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=test_size, random_state=42)
    # Fit preprocessing only on training data to avoid leakage.
    X_train_t = pre.fit_transform(X_train)
    X_test_t = pre.transform(X_test)
    try:
        names = pre.get_feature_names_out()
    except Exception:
        names = np.array([f"feature_{i}" for i in range(X_train_t.shape[1])])
    return X_train_t, X_test_t, y_train, y_test, names

def evaluate_regression(X_train, X_test, y_train, y_test, n_estimators=200):
    model = RandomForestRegressor(n_estimators=n_estimators, random_state=42, n_jobs=-1, min_samples_leaf=1)
    model.fit(X_train, y_train)
    pred = model.predict(X_test)
    rmse = float(np.sqrt(mean_squared_error(y_test, pred)))
    r2 = float(r2_score(y_test, pred)) if len(y_test) > 1 else float("nan")
    importance = pd.DataFrame({"Feature": model.feature_names_in_ if hasattr(model,"feature_names_in_") else [f"Feature {i+1}" for i in range(X_train.shape[1])],
                               "Importance": model.feature_importances_})
    return {"mae":float(mean_absolute_error(y_test,pred)), "rmse":rmse, "r2":r2,
            "y_test":np.asarray(y_test), "predictions":pred, "importance":importance}

def detect_anomalies(df, features, contamination=0.05):
    if not features:
        raise ValueError("Select at least one numeric feature.")
    data = df[features].apply(pd.to_numeric,errors="coerce")
    data = data.replace([np.inf,-np.inf],np.nan)
    if data.dropna(how="all").shape[0] < 5:
        raise ValueError("At least five rows with numeric values are required.")
    imputed = data.fillna(data.median()).fillna(0)
    model = IsolationForest(contamination=contamination, random_state=42, n_estimators=200)
    labels = model.fit_predict(imputed)
    result = df.copy()
    result["Anomaly"] = np.where(labels == -1, "Anomaly", "Normal")
    result["Anomaly score"] = -model.score_samples(imputed)
    return result.sort_values("Anomaly score",ascending=False)

def build_recommendations(df):
    p = profile_dataset(df)
    items = []
    if p["missing_pct"] > 0:
        items.append({"title":"Review incomplete records",
            "detail":f"{p['missing_cells']:,} missing cells ({p['missing_pct']:.1f}% of all cells). Check whether missingness is systematic before imputing or excluding data."})
    if p["duplicates"] > 0:
        items.append({"title":"Investigate duplicate rows",
            "detail":f"{p['duplicates']:,} exact duplicate rows detected. Confirm whether these represent repeated events or accidental duplication."})
    numeric = df.select_dtypes(include=np.number)
    for col in numeric.columns[:8]:
        s=pd.to_numeric(numeric[col],errors="coerce").dropna()
        if len(s)>=8 and s.mean()!=0:
            cv=float(s.std()/abs(s.mean()))
            if cv>1.0:
                items.append({"title":f"High variation in {col}",
                    "detail":f"The coefficient of variation is {cv:.2f}. Segment this metric by time, region or category to understand the drivers."})
    if not items:
        items.append({"title":"Maintain data-quality controls",
            "detail":"No missing cells or exact duplicate rows were detected. Continue monitoring incoming records and validate business definitions."})
    return items

def format_number(value):
    try:
        v=float(value)
        if not np.isfinite(v): return "N/A"
        if abs(v)>=1_000_000: return f"{v/1_000_000:,.2f}M"
        if abs(v)>=1_000: return f"{v:,.2f}"
        return f"{v:,.2f}"
    except Exception:
        return str(value)
