# src/run_demo.py
import subprocess
import os

BASE_DIR = os.path.dirname(__file__)
DATA_FILE = os.path.join(BASE_DIR, "..", "data", "customers_sample.csv")
OUTPUT_FILE = os.path.join(BASE_DIR, "..", "outputs", "predictions.csv")

def main():
    print("Schritt 1: Trainiere Beispielmodell...")
    subprocess.run(["python", os.path.join(BASE_DIR, "train.py")], check=True)

    print("\n Schritt 2: Führe Scoring auf Beispiel-CSV durch...")
    subprocess.run([
        "python", "-m", "src.score",
        "--input", DATA_FILE,
        "--output", OUTPUT_FILE,
        "--model", os.path.join(BASE_DIR, "..", "models", "churn_pipeline.joblib"),
        "--metadata", os.path.join(BASE_DIR, "..", "models", "metadata.json")
    ], check=True)

    print(f"\n✅ Fertig! Predictions unter: {OUTPUT_FILE}")

if __name__ == "__main__":
    main()