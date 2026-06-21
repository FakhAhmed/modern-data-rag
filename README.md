# Modern Data Stack & Advanced RAG (IT Support)

Ce projet implémente une architecture complète de traitement de données (ELT) couplée à un système d'IA générative (Advanced RAG). Il intègre un audit mathématique en temps réel pour évaluer et bloquer les hallucinations de l'IA, appliqué à l'analyse de tickets de support informatique.

- **Lien de l'application :** [IT Support - AI Analytics](https://modern-data-rag-app-342992646165.europe-west9.run.app)

## 🚀 Fonctionnalités Clés
- **Advanced RAG (Retrieval-Augmented Generation) :** Utilisation de **LlamaIndex** pour une recherche sémantique de haute précision sur une base de données de tickets informatiques.
- **Audit Mathématique (MLOps) :** Intégration d'évaluateurs en temps réel (type RAGAS) pour calculer visuellement le score de **Fidélité** (zéro hallucination) et de **Pertinence** de chaque réponse générée par l'IA.
- **Data Engineering (ELT) :** Pipeline de transformation des données brutes avec **dbt Core** directement dans Google BigQuery (nettoyage, standardisation des dates, tests d'intégrité).
- **Vectorisation Scalable :** Utilisation du modèle d'embedding de Google (Vertex AI) et stockage dans **Qdrant Cloud** pour une recherche vectorielle ultra-rapide.
- **Automatisation 100% Serverless :** Remplacement des orchestrateurs lourds (comme Airflow) par une architecture native GCP combinant **Cloud Scheduler** et **Cloud Run Job** pour une exécution quotidienne automatisée et économique.
- **Expérience Utilisateur (UI/UX) :** Interface **Streamlit** fluide incluant un tableau de bord d'audit IA, l'affichage direct des sources (tickets de référence) et la gestion asynchrone sécurisée.

## 🏗️ Architecture Technique
- **LLM & Embeddings :** Gemini 3.5 Flash & VertexTextEmbedding-004 (Google Vertex AI)
- **Framework RAG & Évaluation :** LlamaIndex
- **Data Warehouse :** Google BigQuery
- **Transformation Data :** dbt (Data Build Tool)
- **Vector Database :** Qdrant Cloud
- **Orchestration & Pipeline :** Google Cloud Scheduler
- **Infrastructure Web & Job :** Google Cloud Run (Service & Job)
- **Conteneurisation :** Architecture Monorepo avec Docker (Séparation App / Pipeline)

## 📁 Structure du Projet
- **`/app/`** : "Le Frontend". Contient l'interface utilisateur Streamlit (`main.py`) et l'affichage du Dashboard d'évaluation mathématique.
- **`/dbt_transform/`** : "L'Usine de Données". Projet dbt complet contenant les modèles SQL de nettoyage (`clean_it_tickets.sql`) et la configuration BigQuery.
- **`/scripts/`** : "Le Laboratoire". Scripts d'ingénierie initiaux pour la génération de fausses données (`generate_mock_data.py`) et les tests d'évaluation d'IA en local (`evaluate_rag.py`).
- **`run_pipeline.py`** : Point d'entrée principal du pipeline de données (déclenche dbt puis l'ingestion vers Qdrant Cloud).
- **`Dockerfile.app` & `Dockerfile.pipeline`** : Fichiers de conteneurisation distincts respectant les meilleures pratiques du modèle Monorepo.
- **`requirements.txt` & `requirements-app.txt`** : Gestion stricte des dépendances Python pour chaque environnement.

## 💡 Pourquoi ce projet ?
Ce PoC démontre la capacité à créer un pont robuste entre l'ingénierie des données classique (Modern Data Stack) et l'IA générative de pointe. Il prouve aux entreprises qu'un RAG peut être mis en production en toute confiance : les données sont propres (grâce à dbt), l'infrastructure est scalable (Serverless GCP), et surtout, les réponses de l'IA sont mesurées et validées mathématiquement pour éviter toute hallucination.