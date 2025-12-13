-- Table: english_trainer.vocabulary

-- DROP TABLE IF EXISTS english_trainer.vocabulary;

CREATE TABLE IF NOT EXISTS english_trainer.vocabulary
(
    id integer NOT NULL GENERATED ALWAYS AS IDENTITY ( INCREMENT 1 START 1 MINVALUE 1 MAXVALUE 2147483647 CACHE 1 ),
    word character varying(50) COLLATE pg_catalog."default",
    meaning character varying(50) COLLATE pg_catalog."default",
    hint character varying(150) COLLATE pg_catalog."default",
    CONSTRAINT vocabulary_pkey PRIMARY KEY (id)
)

TABLESPACE pg_default;