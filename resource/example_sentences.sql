-- Table: english_trainer.example_sentences

-- DROP TABLE IF EXISTS english_trainer.example_sentences;

CREATE TABLE IF NOT EXISTS english_trainer.example_sentences
(
    id integer NOT NULL GENERATED ALWAYS AS IDENTITY ( INCREMENT 1 START 1 MINVALUE 1 MAXVALUE 2147483647 CACHE 1 ),
    vocab_id integer,
    sentence character varying(200) COLLATE pg_catalog."default",
    CONSTRAINT example_sentences_pkey PRIMARY KEY (id),
    CONSTRAINT fk_vocabulary FOREIGN KEY (vocab_id)
        REFERENCES english_trainer.vocabulary (id) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION
)

TABLESPACE pg_default;