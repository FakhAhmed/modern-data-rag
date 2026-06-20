# On part d'un Python officiel et léger
FROM python:3.11-slim

# On définit le dossier de travail dans le conteneur
WORKDIR /app

# On copie JUSTE le fichier léger pour l'application
COPY requirements-app.txt .
RUN pip install --no-cache-dir -r requirements-app.txt

# On copie le reste de notre code (dossiers app, scripts, etc.)
COPY . .

# On expose le port de Streamlit
EXPOSE 8080

# La commande pour démarrer le site
CMD ["streamlit", "run", "app/main.py", "--server.port=8080", "--server.address=0.0.0.0"]
