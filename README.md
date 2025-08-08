# churn-sentinel

**Kurz:** Dieses Projekt demonstriert, wie Unternehmen mit minimalem Code-Aufwand ein bestehendes Churn-Modell auf neue Kundendaten anwenden können. Es eignet sich sowohl für Prototyping als auch als Basis für produktive Batch-Scoring-Pipelines.

## Ordnerstruktur

churn-sentinel/
├─ data/           # Beispiel-CSV-Dateien
├─ models/         # gespeicherte Modelle + metadata.json
├─ outputs/        # Ergebnisdateien mit Predictions
├─ src/            # Quellcode: train.py, score.py, utils.py
├─ tests/          # einfache Unit Tests
├─ requirements.txt
├─ Dockerfile
└─ README.md

## Quickstart

1. Klone / erstelle das Repo und wechsle in den Ordner:
```bash
git clone git@github.com:sik84/churn-sentinel.git
cd churn-sentinel
```

2. Virtuelle Umgebung & Abhängigkeiten

```bash
python -m venv .venv
source .venv/bin/activate      # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

3. Trainiere ein Beispielmodell (schreibt models/churn_pipeline.joblib und models/metadata.json):

```bash
python src/train.py
```

4. Beispiel-Input liegt in data/customers_sample.csv. Scoring:
```bash
python -m src.score --input data/customers_sample.csv --output outputs/predictions.csv --model models/churn_pipeline.joblib --metadata models/metadata.json
```

5. Installation via Docker
```bash
docker build -t churn-sentinel .
docker run --rm -v $(pwd)/data:/app/data -v $(pwd)/outputs:/app/outputs churn-sentinel
```