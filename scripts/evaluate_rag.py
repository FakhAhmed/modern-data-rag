import google.auth
from llama_index.core import VectorStoreIndex, Settings
from llama_index.vector_stores.qdrant import QdrantVectorStore
from qdrant_client import QdrantClient
from llama_index.embeddings.vertex import VertexTextEmbedding
from llama_index.llms.vertex import Vertex
from llama_index.core.evaluation import FaithfulnessEvaluator, RelevancyEvaluator

# 1. Configuration GCP
PROJECT_ID = "modern-data-rag"
credentials, project = google.auth.default()

print("🔌 Initialisation du RAG et de l'Évaluateur...")

# 2. Configuration de l'Élève ET du Professeur (Gemini 3.5)
embed_model = VertexTextEmbedding(model_name="text-embedding-004", project=PROJECT_ID, location="europe-west9", credentials=credentials)
llm = Vertex(model="gemini-3.5-flash", project=PROJECT_ID, location="global", credentials=credentials, max_tokens=8192)

Settings.context_window = 1048576
Settings.num_output = 8192
Settings.embed_model = embed_model
Settings.llm = llm

# 3. Chargement de la base Qdrant
qdrant_client = QdrantClient(path="./qdrant_data")
vector_store = QdrantVectorStore(client=qdrant_client, collection_name="it_tickets")
index = VectorStoreIndex.from_vector_store(vector_store=vector_store)
query_engine = index.as_query_engine(similarity_top_k=3)

# 4. Les Correcteurs Mathématiques
# Faithfulness : Vérifie si l'IA hallucine ou reste fidèle aux tickets
faithfulness_evaluator = FaithfulnessEvaluator(llm=llm)
# Relevancy : Vérifie si la réponse a bien un rapport avec la question
relevancy_evaluator = RelevancyEvaluator(llm=llm)

# 5. L'Examen !
question = "Quels sont les problèmes fréquents avec les imprimantes dans nos tickets ?"

print(f"\n🧑‍💻 Question : {question}")
print("🤖 L'IA génère sa réponse...")
response = query_engine.query(question)
print(f"✨ Réponse générée : {response.response}\n")

print("📊 Correction de la copie en cours...")

# Évaluation 1
eval_faith = faithfulness_evaluator.evaluate_response(query=question, response=response)
print(f"✅ Fidélité (Pas d'hallucination) : {'RÉUSSI' if eval_faith.passing else 'ÉCHOUÉ'} (Score: {eval_faith.score})")

# Évaluation 2
eval_rel = relevancy_evaluator.evaluate_response(query=question, response=response)
print(f"✅ Pertinence (Répond à la question) : {'RÉUSSI' if eval_rel.passing else 'ÉCHOUÉ'} (Score: {eval_rel.score})")