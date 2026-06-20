{{ config(materialized='table') }}

WITH raw_tickets AS (
    -- La macro {{ target.project }} permet à dbt d'injecter automatiquement ton ID de projet GCP
    SELECT * FROM `{{ target.project }}.it_support_raw.raw_tickets`
)

SELECT
    ticket_id,
    category,
    -- Nettoyage du texte : on enlève les espaces inutiles au début et à la fin
    TRIM(description) AS description,
    
    -- Standardisation absolue de la priorité (règles de gestion métier)
    CASE 
        WHEN UPPER(TRIM(priority)) IN ('HAUTE', 'URGENT') THEN 'Haute'
        WHEN UPPER(TRIM(priority)) IN ('MOYENNE') THEN 'Moyenne'
        WHEN UPPER(TRIM(priority)) IN ('BASSE', 'FAIBLE') THEN 'Basse'
        ELSE 'Non spécifiée'
    END AS priority,
    
    -- Gestion des dates nulles
    COALESCE(CAST(created_at AS STRING), 'Date inconnue') AS created_date

FROM raw_tickets
WHERE ticket_id IS NOT NULL