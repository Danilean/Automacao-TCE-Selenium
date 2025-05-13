-- View: public.tce_formatados

-- DROP VIEW public.tce_formatados;

CREATE OR REPLACE VIEW public.tce_formatados
 AS
 SELECT row_number() OVER (ORDER BY (to_date("Data", 'MM/YYYY'::text)), "Ente", "UG", "Tipo") AS id,
    to_date("Data", 'MM/YYYY'::text) AS data_formatada,
    "Ente" AS entidade,
    "UG" AS unidade_gestora,
    "Tipo" AS tipo,
    NULLIF("Valores", '-'::text)::double precision AS valores,
        CASE
            WHEN "Clientes" = 'Betha Sistemas'::text THEN true
            ELSE false
        END AS is_cliente_betha,
        CASE
            WHEN "Tipo" <> 'Situações de Obras/Serviços de Engenharia em Atraso'::text THEN
            CASE
                WHEN NULLIF("Valores", '-'::text)::double precision IS NULL THEN false
                WHEN NULLIF("Valores", '-'::text)::double precision = 0::double precision THEN true
                WHEN NULLIF("Valores", '-'::text)::double precision > 0::double precision THEN false
                ELSE NULL::boolean
            END
            WHEN "Tipo" = 'Situações de Obras/Serviços de Engenharia em Atraso'::text THEN
            CASE
                WHEN NULLIF("Valores", '-'::text)::double precision IS NULL THEN false
                WHEN NULLIF("Valores", '-'::text)::double precision = 0::double precision THEN false
                WHEN NULLIF("Valores", '-'::text)::double precision > 0::double precision THEN true
                ELSE NULL::boolean
            END
            ELSE NULL::boolean
        END AS is_problema
   FROM "DadosTCE" tc;

ALTER TABLE public.tce_formatados
    OWNER TO postgres;

GRANT SELECT ON TABLE public.tce_formatados TO "diogo.lopes";
GRANT ALL ON TABLE public.tce_formatados TO postgres;

