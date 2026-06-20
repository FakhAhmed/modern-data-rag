import google.auth
from qdrant_client import QdrantClient
from llama_index.core import VectorStoreIndex, Settings
from llama_index.vector_stores.qdrant import QdrantVectorStore
from llama_index.embeddings.vertex import VertexTextEmbedding
from llama_index.llms.vertex import Vertex

# 1. Configuration (Vérifie toujours ton ID)
PROJECT_ID = "modern-data-rag"
LOCATION = "europe-west9"
credentials, project = google.auth.default()

print("🔌 Connexion aux modèles d'IA...")

# 2. Configuration Globale de LlamaIndex (Embedding + LLM)
embed_model = VertexTextEmbedding(
    model_name="text-embedding-004", 
    project=PROJECT_ID,
    location="europe-west9", 
    credentials=credentials
)

# On utilise Gemini 3.5 Flash comme cerveau pour rédiger la réponse
llm = Vertex(
    model="gemini-3.5-flash", 
    project=PROJECT_ID,
    location="global",
    credentials=credentials,
    max_tokens=8192 
)

Settings.context_window = 1048576  # On lui dit d'arrêter de s'inquiéter pour la mémoire
Settings.num_output = 8192

Settings.embed_model = embed_model
Settings.llm = llm

# 3. Connexion à notre base de données locale
print("📂 Chargement de la base de connaissances IT...")
qdrant_client = QdrantClient(path="./qdrant_data")
vector_store = QdrantVectorStore(client=qdrant_client, collection_name="it_tickets")

# On charge l'index existant (sans re-vectoriser !)
index = VectorStoreIndex.from_vector_store(vector_store=vector_store)

# 4. Création du moteur de RAG
query_engine = index.as_query_engine(similarity_top_k=5) # On lui demande de lire les 5 meilleurs tickets

# 5. Le Test
question = "Quels sont les problèmes les plus fréquents liés aux imprimantes dans nos tickets, et quelle est généralement leur priorité ?"
print(f"\n🧑‍💻 Utilisateur : {question}")
print("🤖 Recherche et génération de la réponse en cours...\n")

response = query_engine.query(question)

print("="*50)
print(f"✨ RÉPONSE DE L'IA :\n{response}")
print("="*50)