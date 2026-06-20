# Modern Data Stack & Advanced RAG (IT Support)

Ce projet implémente une architecture complète de traitement de données (ELT) couplée à un système d'IA générative (RAG) avec évaluation mathématique des hallucinations, appliqué à l'analyse de tickets de support informatique.

## 🏗️ Architecture Technique

1. **Ingestion & Stockage (Extract & Load) :** Données brutes chargées dans Google BigQuery.
2. **Transformation (ELT) :** Nettoyage et modélisation des données avec **dbt** directement dans le Data Warehouse.
3. **Orchestration :** L'ensemble du pipeline de données est automatisé et planifié par **Apache Airflow**.
4. **Vectorisation & IA :** Création des embeddings et stockage dans la base vectorielle **Qdrant**.
5. **RAG Avancé :** Interrogation des données métiers avec **LlamaIndex**.
6. **MLOps & Évaluation :** Mesure mathématique des performances du RAG (Fidélité, Pertinence) via le framework **RAGAS**.

## 📂 Structure du Projet (En cours)
- `/data` : Données sources brutes (ignorées par Git).
- `/scripts` : Scripts utilitaires (génération de données mockées).