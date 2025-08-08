import argparse
import os
import sys
import pandas as pd
import joblib
import json
from src.utils import recommend
from logger import get_logger

logger = get_logger(__name__)

def file_exists(path):
    if not os.path.isfile(path):
        raise argparse.ArgumentTypeError(f"Datei nicht gefunden: {path}")
    return path

def parse_args():
    parser = argparse.ArgumentParser(
        description="Churn-Risk-Engine: Liest Kundendaten, wendet Modell an, schreibt Vorhersagen."
    )
    parser.add_argument(
        "--input", "-i",
        type=file_exists,
        required=True,
        help="Pfad zur Input-CSV mit Kundendaten."
    )
    parser.add_argument(
        "--output", "-o",
        default="outputs/predictions.csv",
        help="Pfad zur Ausgabe-CSV. Standard: outputs/predictions.csv"
    )
    parser.add_argument(
        "--model", "-m",
        type=file_exists,
        required=True,
        help="Pfad zum gespeicherten Modell (joblib-Datei)."
    )
    parser.add_argument(
        "--metadata", "-d",
        type=file_exists,
        required=True,
        help="Pfad zur Metadaten-Datei (JSON)."
    )
    return parser.parse_args()

def main():
    args = parse_args()

    logger.info(f"Lade Modell von: {args.model}")
    model = joblib.load(args.model)

    logger.info(f"Lade Metadaten von: {args.metadata}")
    with open(args.metadata) as f:
        metadata = json.load(f)

    logger.info(f"Lade Kundendaten von: {args.input}")
    df = pd.read_csv(args.input)

    features = metadata["feature_columns"]
    threshold = metadata.get("threshold", 0.5)

    X = df[features]

    churn_proba = model.predict_proba(X)[:, 1]
    df["Churn_Probability"] = churn_proba
    df["Churn_Prediction"] = (churn_proba > threshold).astype(int)
    df["Recommendation"] = df["Churn_Probability"].apply(lambda x: recommend(x, threshold))

    df.to_csv(args.output, index=False)
    logger.info(f"Wrote predictions to {args.output}")

if __name__ == "__main__":
    main()
