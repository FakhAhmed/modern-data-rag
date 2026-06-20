import os
import streamlit as st
import google.auth
from dotenv import load_dotenv
from qdrant_client import QdrantClient
from llama_index.core import VectorStoreIndex, Settings
from llama_index.vector_stores.qdrant import QdrantVectorStore
from llama_index.embeddings.vertex import VertexTextEmbedding
from llama_index.llms.vertex import Vertex

# Chargement des secrets
load_dotenv()

st.set_page_config(page_title="IT Support - AI Analytics", page_icon="🤖", layout="wide")
st.title("🤖 Assistant IA - Support Technique IT")

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
    
    qdrant_client = QdrantClient(url=os.getenv("QDRANT_URL"), api_key=os.getenv("QDRANT_API_KEY"))
    vector_store = QdrantVectorStore(client=qdrant_client, collection_name="it_tickets")
    index = VectorStoreIndex.from_vector_store(vector_store=vector_store)
    return index.as_query_engine(similarity_top_k=4)

query_engine = init_rag_engine()

with st.sidebar:
    st.header("⚙️ Architecture du Système")
    st.success("📦 dbt Pipeline : OK")
    st.success("☁️ Qdrant Cloud : Connecté")
    st.info("🧠 LLM Engine : Gemini 3.5 Flash")
    st.caption("Données synchronisées via BigQuery")
    if st.button("🗑️ Effacer l'historique"):
        st.session_state.messages = []

# --- GESTION DE L'HISTORIQUE DE CHAT ---
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "assistant", "content": "Bonjour ! Je suis connecté à la base de tickets Qdrant. Que voulez-vous savoir ?"}]

# Afficher les messages précédents
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# --- BARRE DE CHAT FIXE EN BAS ---
if prompt := st.chat_input("💡 Posez votre question sur les tickets de support..."):
    # 1. Afficher la question de l'utilisateur
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # 2. Générer et afficher la réponse
    with st.chat_message("assistant"):
        with st.spinner("🧠 Analyse des tickets Cloud en cours..."):
            try:
                response = query_engine.query(prompt)
                st.markdown(response.response)
                
                with st.expander("🔍 Voir les tickets sources"):
                    for i, node in enumerate(response.source_nodes):
                        st.info(f"**Ticket #{i+1}** (Similarité: {node.score:.4f})\n\n{node.node.text}")
                
                # 3. Sauvegarder la réponse dans l'historique
                st.session_state.messages.append({"role": "assistant", "content": response.response})
            except Exception as e:
                st.error(f"Erreur : {e}")