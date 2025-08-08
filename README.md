# churn-sentinel

**Kurz:**  
Dieses Projekt demonstriert, wie Unternehmen mit minimalem Code-Aufwand ein bestehendes Churn-Modell auf neue Kundendaten anwenden können. Es eignet sich sowohl für schnelles Prototyping als auch als Basis für produktive Batch-Scoring-Pipelines.

## Ordnerstruktur

churn-sentinel/  
├─ data/           # Beispiel-CSV-Dateien mit Kundendaten  
├─ models/         # Gespeicherte Modelle & Metadaten (z.B. churn_pipeline.joblib, metadata.json)  
├─ outputs/        # Ergebnisdateien mit Predictions (z.B. predictions.csv)  
├─ src/            # Quellcode: train.py (Modelltraining), score.py (Scoring), utils.py (Hilfsfunktionen)  
├─ tests/          # Unit Tests für einzelne Funktionen  
├─ requirements.txt  
├─ Dockerfile  
└─ README.md  

## Quickstart

1. Repository klonen und ins Projektverzeichnis wechseln:  
```bash
git clone git@github.com:sik84/churn-sentinel.git
cd churn-sentinel

2. Virtuelle Umgebung & Abhängigkeiten installieren:

```bash
python -m venv .venv
source .venv/bin/activate      # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

3. Trainiere ein Beispielmodell (schreibt models/churn_pipeline.joblib und models/metadata.json):

```bash
python src/train.py
```

4. Mit dem trainierten Modell Scoring auf Beispiel-Daten ausführen (Ergebnis wird in outputs/predictions.csv geschrieben):

```bash
python -m src.score --input data/customers_sample.csv --output outputs/predictions.csv --model models/churn_pipeline.joblib --metadata models/metadata.json
```

5. Ausführung der Analyse in einem Container

**Docker-Image bauen**
```bash
docker build -t churn-sentinel .
```

**Scoring im Container starten**
```bash
docker run --rm churn-sentinel --input data/customers_sample.csv --output outputs/predictions.csv --model models/churn_pipeline.joblib --metadata models/metadata.json
```

**Volume erstellen, falls Ausgabedateien lokal betrachtet werden wollen**
```bash
docker run --rm -v $(pwd)/outputs:/app/outputs churn-sentinel --input data/customers_sample.csv --output outputs/predictions.csv --model models/churn_pipeline.joblib --metadata models/metadata.json
```

---

## Hinweise

Input-Daten: Die CSV-Dateien in data/ müssen dieselben Features enthalten, die im Modelltraining verwendet wurden.

Metadaten: metadata.json enthält wichtige Infos, z.B. welche Spalten als Features genutzt werden und welcher Schwellenwert (threshold) für die Churn-Entscheidung gilt.

Erweiterungen: Logging, Tests und eine benutzerfreundliche CLI sind bereits implementiert — so kannst du das Projekt einfach anpassen und produktiv nutzen.