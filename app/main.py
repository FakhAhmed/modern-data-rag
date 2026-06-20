import streamlit as st
import google.auth
from qdrant_client import QdrantClient
from llama_index.core import VectorStoreIndex, Settings
from llama_index.vector_stores.qdrant import QdrantVectorStore
from llama_index.embeddings.vertex import VertexTextEmbedding
from llama_index.llms.vertex import Vertex

# Configuration de la page Streamlit
st.set_page_config(page_title="IT Support - AI Analytics", page_icon="🤖", layout="wide")

st.title("🤖 Assistant IA - Support Technique IT")
st.subheader("Posez vos questions à notre base de connaissances Modern Data RAG")

# Initialisation de la connexion IA (Mise en cache pour éviter de recharger à chaque clic)
@st.cache_resource
def init_rag_engine():
    PROJECT_ID = "modern-data-rag"
    LOCATION = "global"
    credentials, project = google.auth.default()
    
    embed_model = VertexTextEmbedding(
        model_name="text-embedding-004", 
        project=PROJECT_ID, 
        location="europe-west9", 
        credentials=credentials
    )
    
    llm = Vertex(
        model="gemini-3.5-flash", 
        project=PROJECT_ID, 
        location=LOCATION, 
        credentials=credentials,
        max_tokens=8192
    )
    
    Settings.context_window = 1048576
    Settings.num_output = 8192
    Settings.embed_model = embed_model
    Settings.llm = llm
    
    qdrant_client = QdrantClient(path="./qdrant_data")
    vector_store = QdrantVectorStore(client=qdrant_client, collection_name="it_tickets")
    index = VectorStoreIndex.from_vector_store(vector_store=vector_store)
    return index.as_query_engine(similarity_top_k=4)

query_engine = init_rag_engine()

# Barre latérale pour afficher les infos du système
with st.sidebar:
    st.header("⚙️ Architecture du Système")
    st.success("📦 dbt Pipeline : OK")
    st.success("🗄️ Qdrant Vector DB : Connecté")
    st.info("🧠 LLM Engine : Gemini 3.5 Flash")
    st.caption("Données synchronisées via BigQuery")

# Zone de chat pour l'utilisateur
question = st.text_input("💡 Quelle est votre question sur les tickets de support ?", 
                         placeholder="Ex: Quels sont les problèmes de VPN les plus urgents ?")

if question:
    with st.spinner("🧠 L'IA analyse les tickets et rédige sa réponse..."):
        try:
            response = query_engine.query(question)
            
            # Affichage de la réponse principale
            st.markdown("### ✨ Réponse de l'IA")
            st.write(response.response)
            
            # Affichage des sources (Les tickets originaux utilisés pour répondre)
            st.markdown("---")
            with st.expander("🔍 Voir les tickets sources extraits de Qdrant"):
                for i, node in enumerate(response.source_nodes):
                    st.info(f"**Ticket Source #{i+1}** (Score de similarité: {node.score:.4f})\n\n{node.node.text}")
                    
        except Exception as e:
            st.error(f"Une erreur est survenue lors de l'appel à Gemini : {e}")