# 1. Utiliser une image Python officielle légère
FROM python:3.11-slim

# 2. Installer les outils système nécessaires (git, dbt, etc.)
RUN apt-get update && apt-get install -y --no-install-recommends \
    git \
    && rm -rf /var/lib/apt/lists/*

# 3. Définir le répertoire de travail
WORKDIR /app

# 4. Copier les dépendances et installer
COPY requirements-app.txt .
# On ajoute dbt-bigquery explicitement si besoin
RUN pip install --no-cache-dir -r requirements-app.txt dbt-bigquery

# 5. Copier tout le code source
COPY . .

# 6. Utiliser ton script comme point d'entrée pour Cloud Run
# On lance le pipeline, et une fois fini, le conteneur s'arrête (parfait pour Cloud Run)
CMD ["python", "run_pipeline.py"]