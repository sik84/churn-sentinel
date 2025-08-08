# Basis-Image mit Python 3.10
FROM python:3.10-slim

# Arbeitsverzeichnis im Container
WORKDIR /app

# Abhängigkeiten kopieren und installieren
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Quellcode kopieren
COPY src ./src
COPY data ./data
COPY models ./models

# Standardkommando, um das Scoring-Skript auszuführen (kann überschrieben werden)
CMD ["python", "-m", "src.score", "--help"]
