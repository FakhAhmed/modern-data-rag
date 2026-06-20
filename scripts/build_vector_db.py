import os
import google.auth
from google.cloud import bigquery
from qdrant_client import QdrantClient
from llama_index.core import Document, VectorStoreIndex, StorageContext
from llama_index.vector_stores.qdrant import QdrantVectorStore
from llama_index.embeddings.vertex import VertexTextEmbedding

# 1. Configuration du projet GCP
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

# 4. Conversion en Documents LlamaIndex
print("📝 Formatage des documents pour l'IA...")
documents = []
for ticket in tickets:
    # Le texte que l'IA va "lire" et vectoriser
    content = f"Catégorie: {ticket['category']}\nPriorité: {ticket['priority']}\nDescription: {ticket['description']}"
    
    # Les métadonnées (très important pour filtrer plus tard)
    metadata = {
        "ticket_id": ticket["ticket_id"],
        "created_date": str(ticket["created_date"])
    }
    
    documents.append(Document(text=content, metadata=metadata))

# 5. Création des Embeddings et stockage dans Qdrant
print("🧠 Vectorisation via Vertex AI en cours (ça peut prendre 1 à 2 minutes)...")


credentials, project = google.auth.default()

# On utilise le modèle d'embedding de Google
embed_model = VertexTextEmbedding(
    model_name="text-embedding-004", 
    project=PROJECT_ID,
    location="europe-west9",
    credentials=credentials
)

# On connecte LlamaIndex à notre Qdrant local
vector_store = QdrantVectorStore(client=qdrant_client, collection_name="it_tickets")
storage_context = StorageContext.from_defaults(vector_store=vector_store)

# LA MAGIE OPÈRE ICI : Envoi du texte à Google, réception des vecteurs, stockage dans Qdrant
index = VectorStoreIndex.from_documents(
    documents, 
    storage_context=storage_context, 
    embed_model=embed_model
)

print("🎉 Indexation terminée avec succès ! La base vectorielle est prête.")