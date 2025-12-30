-- Table: english_trainer.training_state

-- DROP TABLE IF EXISTS english_trainer.training_state;

CREATE TABLE IF NOT EXISTS english_trainer.training_state
(
    id integer NOT NULL GENERATED ALWAYS AS IDENTITY ( INCREMENT 1 START 1 MINVALUE 1 MAXVALUE 2147483647 CACHE 1 ),
    vocab_id integer,
    streak smallint,
    last_review date,
    next_review date,
    confidence smallint,
    CONSTRAINT training_state_pkey PRIMARY KEY (id),
    CONSTRAINT fk_vocabulary FOREIGN KEY (vocab_id)
        REFERENCES english_trainer.vocabulary (id) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION
        NOT VALID,
    CONSTRAINT chk_streak CHECK (streak >= 0 AND streak <= 5),
    CONSTRAINT chk_confidence CHECK (confidence >= 0 AND confidence <= 3)
)

TABLESPACE pg_default;
-- Index: idx_training_next_review

-- DROP INDEX IF EXISTS english_trainer.idx_training_next_review;

CREATE INDEX IF NOT EXISTS idx_training_next_review
    ON english_trainer.training_state USING btree
    (next_review ASC NULLS LAST)
    TABLESPACE pg_default;

-- Trigger: trg_update_next_review

-- DROP TRIGGER IF EXISTS trg_update_next_review ON english_trainer.training_state;

CREATE OR REPLACE TRIGGER trg_update_next_review
    BEFORE UPDATE OF streak, last_review, confidence
    ON english_trainer.training_state
    FOR EACH ROW
    EXECUTE FUNCTION public.trg_calculate_next_review();