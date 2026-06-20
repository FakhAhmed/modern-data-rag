import os
from google.cloud import bigquery
from qdrant_client import QdrantClient

# 1. Configuration du projet GCP
# Remplace par TON vrai ID de projet GCP
PROJECT_ID = "modern-data-rag" 
DATASET_ID = "it_support_clean"
TABLE_ID = "clean_it_tickets"

print("🚀 Démarrage du pipeline d'ingestion vectorielle...")

# 2. Initialisation des clients
bq_client = bigquery.Client(project=PROJECT_ID)

# Initialisation de Qdrant en local (créera un dossier 'qdrant_data' dans ton projet)
qdrant_client = QdrantClient(path="./qdrant_data")

# 3. Requête pour récupérer les données propres
query = f"""
    SELECT ticket_id, category, description, priority, created_date 
    FROM `{PROJECT_ID}.{DATASET_ID}.{TABLE_ID}`
"""

print("📊 Téléchargement des données depuis BigQuery...")
query_job = bq_client.query(query)
results = query_job.result()

tickets = [dict(row) for row in results]
print(f"✅ {len(tickets)} tickets récupérés avec succès !")