CREATE OR REPLACE FUNCTION trg_calculate_next_review()
RETURNS TRIGGER
LANGUAGE plpgsql
AS $$
DECLARE
    v_interval_base INTEGER;
    v_multiplier NUMERIC;
    v_days_to_next INTEGER;
BEGIN
    -- Intervalo base por streak
    v_interval_base := CASE NEW.streak
        WHEN 0 THEN 1
        WHEN 1 THEN 2
        WHEN 2 THEN 4
        WHEN 3 THEN 7
        WHEN 4 THEN 14
        WHEN 5 THEN 30
        ELSE 30
    END;

    -- Multiplicador por confidence
    v_multiplier := CASE NEW.confidence
        WHEN 0 THEN 0.8
        WHEN 1 THEN 1.0
        WHEN 2 THEN 1.25
        ELSE 1.0
    END;

    -- Calcula dias até a próxima revisão
    v_days_to_next := ROUND(v_interval_base * v_multiplier);

    IF v_days_to_next < 1 THEN
        v_days_to_next := 1;
    END IF;

    -- Atualiza apenas o next_review
    NEW.next_review := NEW.last_review + v_days_to_next;

    RETURN NEW;
END;
$$;
