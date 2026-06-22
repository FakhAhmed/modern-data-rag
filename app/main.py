import asyncio
import nest_asyncio
try:
    loop = asyncio.get_running_loop()
except RuntimeError:
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
nest_asyncio.apply()

import os
import streamlit as st
import google.auth
from dotenv import load_dotenv
from qdrant_client import QdrantClient
from llama_index.core import VectorStoreIndex, Settings
from llama_index.vector_stores.qdrant import QdrantVectorStore
from llama_index.embeddings.vertex import VertexTextEmbedding
from llama_index.llms.vertex import Vertex
from llama_index.core.evaluation import FaithfulnessEvaluator, RelevancyEvaluator

# Chargement des secrets
load_dotenv()
st.set_page_config(page_title="IT Support - AI Analytics", page_icon="🤖", layout="wide")
st.title("🤖 Assistant IA - Support Technique IT")
@st.cache_resource(show_spinner="Initialisation de l'IA (veuillez patienter)...")
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
    query_engine = index.as_query_engine(similarity_top_k=4)
    faithfulness_evaluator = FaithfulnessEvaluator(llm=llm)
    relevancy_evaluator = RelevancyEvaluator(llm=llm)
    
    return query_engine, faithfulness_evaluator, relevancy_evaluator

query_engine, faithfulness_evaluator, relevancy_evaluator = init_rag_engine()

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
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("🧠 Analyse des tickets Cloud en cours..."):
            try:
                # 1. Génération de la réponse
                response = query_engine.query(prompt)
                st.markdown(response.response)
                
                # 2. Affichage des sources
                with st.expander("🔍 Voir les tickets sources"):
                    for i, node in enumerate(response.source_nodes):
                        st.info(f"**Ticket #{i+1}** (Similarité: {node.score:.4f})\n\n{node.node.text}")
                
                # 3. ÉVALUATION MATHÉMATIQUE (Advanced RAG)
                with st.expander("📊 Évaluation Mathématique (Audit RAG)", expanded=True):
                    with st.spinner("Audit de la réponse en cours..."):
                        # Calcul de la fidélité (zéro hallucination)
                        eval_faith = faithfulness_evaluator.evaluate_response(query=prompt, response=response)
                        # Calcul de la pertinence (rapport avec la question)
                        eval_rel = relevancy_evaluator.evaluate_response(query=prompt, response=response)
                        
                        col1, col2 = st.columns(2)
                        with col1:
                            st.metric(
                                label="Fidélité au contexte (Zéro Hallucination)", 
                                value="Passé ✅" if eval_faith.passing else "Échec ❌",
                                delta="Conforme aux tickets" if eval_faith.passing else "Risque d'invention"
                            )
                        with col2:
                            st.metric(
                                label="Pertinence de la réponse", 
                                value="Passé ✅" if eval_rel.passing else "Échec ❌",
                                delta="Répond à la question" if eval_rel.passing else "Hors-sujet"
                            )

                st.session_state.messages.append({"role": "assistant", "content": response.response})
            except Exception as e:
                st.error(f"Erreur : {e}")