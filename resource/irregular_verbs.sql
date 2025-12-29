-- Table: english_trainer.irregular_verbs

-- DROP TABLE IF EXISTS english_trainer.irregular_verbs;

CREATE TABLE IF NOT EXISTS english_trainer.irregular_verbs
(
    id integer NOT NULL GENERATED ALWAYS AS IDENTITY ( INCREMENT 1 START 1 MINVALUE 1 MAXVALUE 2147483647 CACHE 1 ),
    regular_form character varying(50) COLLATE pg_catalog."default",
	past_simple character varying(50) COLLATE pg_catalog."default",
	past_participle character varying(50) COLLATE pg_catalog."default",
    CONSTRAINT irregular_verbs_pkey PRIMARY KEY (id)
)

TABLESPACE pg_default;