import pandas as pd
import numpy as np
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
import joblib
import json
import os
from datetime import datetime
from logger import get_logger

logger = get_logger(__name__)


def generate_synthetic(n=1000):
    np.random.seed(42)
    df = pd.DataFrame({
        "customer_id": [f"CUST_{i:06d}" for i in range(n)],
        "tenure_months": np.random.randint(0, 72, size=n),
        "monthly_charges": np.round(np.random.uniform(20, 120, size=n), 2),
        "total_charges": lambda x: x["tenure_months"] * x["monthly_charges"],
        "contract_type": np.random.choice(["month-to-month", "one-year", "two-year"], size=n),
        "internet_service": np.random.choice(["DSL", "Fiber optic", "None"], size=n),
        "payment_method": np.random.choice(["Electronic check", "Credit card", "Bank transfer", "Mailed check"], size=n),
        "num_support_calls": np.random.poisson(2, size=n),
        "has_paperless_billing": np.random.choice([0, 1], size=n),
    })
    # calculate total_charges explicitly
    df["total_charges"] = df["tenure_months"] * df["monthly_charges"]
    # create binary target with some logic
    df["target"] = ((df["contract_type"] == "month-to-month") & (df["num_support_calls"] > 3)).astype(int)
    return df

def main():
    # Ordner sicherstellen
    os.makedirs("models", exist_ok=True)

    df = generate_synthetic()

    feature_cols = [
        "tenure_months",
        "monthly_charges",
        "total_charges",
        "contract_type",
        "internet_service",
        "payment_method",
        "num_support_calls",
        "has_paperless_billing"
    ]

    target_col = "target"

    X = df[feature_cols]
    y = df[target_col]

    numeric_features = ["tenure_months", "monthly_charges", "total_charges", "num_support_calls", "has_paperless_billing"]
    categorical_features = ["contract_type", "internet_service", "payment_method"]

    numeric_transformer = StandardScaler()
    categorical_transformer = OneHotEncoder(handle_unknown="ignore")

    preprocessor = ColumnTransformer(
        transformers=[
            ("num", numeric_transformer, numeric_features),
            ("cat", categorical_transformer, categorical_features),
        ]
    )

    clf = Pipeline([
        ("preprocessor", preprocessor),
        ("classifier", LogisticRegression(max_iter=1000)),
    ])

    clf.fit(X, y)

    model_path = "models/churn_pipeline.joblib"
    joblib.dump(clf, model_path)

    metadata = {
        "project": "churn-sentinel",
        "model_name": "logistic_demo",
        "model_version": "v0.1",
        "created_at": datetime.utcnow().isoformat() + "Z",
        "feature_columns": feature_cols,
        "id_column": "customer_id",
        "target_column": target_col,
        "threshold": 0.5
    }

    with open("models/metadata.json", "w") as f:
        json.dump(metadata, f, indent=2)

    logger.info(f"Saved model to {model_path}")
    logger.info("Saved metadata to models/metadata.json")

if __name__ == "__main__":
    main()
