{{ config(materialized='table') }}

WITH raw_tickets AS (
    SELECT * FROM `{{ target.project }}.it_support_raw.raw_tickets`
)

SELECT
    ticket_id,
    category,
    
    -- Nettoyage du texte : On met tout en minuscules pour calmer les textes en MAJUSCULES
    LOWER(TRIM(description)) AS description,
    
    -- Standardisation absolue de la priorité
    CASE 
        WHEN UPPER(TRIM(priority)) IN ('HAUTE', 'URGENT') THEN 'Haute'
        WHEN UPPER(TRIM(priority)) IN ('MOYENNE') THEN 'Moyenne'
        WHEN UPPER(TRIM(priority)) IN ('BASSE', 'FAIBLE') THEN 'Basse'
        ELSE 'Non spécifiée'
    END AS priority,
    
    -- La magie dbt : On tente de parser tous les formats tordus en un vrai format (YYYY-MM-DD)
    COALESCE(
        CAST(SAFE.PARSE_DATE('%Y-%m-%d', created_at) AS STRING),
        CAST(SAFE.PARSE_DATE('%d/%m/%Y', created_at) AS STRING),
        CAST(SAFE.PARSE_DATE('%b %d %Y', created_at) AS STRING),
        CAST(CAST(SAFE.PARSE_DATETIME('%Y/%m/%d %H:%M:%S', created_at) AS DATE) AS STRING),
        'Date inconnue'
    ) AS created_date

FROM raw_tickets
WHERE ticket_id IS NOT NULL