CREATE OR REPLACE VIEW public.tce_formatados AS
WITH dados_deduplicados AS (
  SELECT *,
         ROW_NUMBER() OVER (
            PARTITION BY "Data", "Ente", "UG", "Tipo", "Valores", "Clientes"
            ORDER BY "Data"
         ) AS rn
  FROM "DadosTCE"
)
SELECT
  ROW_NUMBER() OVER (ORDER BY to_date("Data", 'MM/YYYY'), "Ente", "UG", "Tipo") AS id,
  to_date("Data", 'MM/YYYY') AS data_formatada,
  "Ente" AS entidade,
  "UG" AS unidade_gestora,
  "Tipo" AS tipo,
  NULLIF("Valores", '-')::double precision AS valores,
  ("Clientes" = 'Betha Sistemas') AS is_cliente_betha,
  CASE
    WHEN "Tipo" = 'Situações de Obras/Serviços de Engenharia em Atraso' THEN
      COALESCE(NULLIF("Valores", '-')::double precision > 0, false)
    ELSE
      COALESCE(NULLIF("Valores", '-')::double precision = 0, false)
  END AS is_problema
FROM dados_deduplicados
WHERE rn = 1;
