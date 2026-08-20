ALTER TABLE finalized_goals
    ADD COLUMN IF NOT EXISTS evaluation_cycle_id INTEGER NULL;

DO $$
BEGIN
    IF NOT EXISTS (
        SELECT 1
        FROM pg_constraint
        WHERE conname = 'fk_finalized_goals_evaluation_cycle'
    ) THEN
        ALTER TABLE finalized_goals
            ADD CONSTRAINT fk_finalized_goals_evaluation_cycle
            FOREIGN KEY (evaluation_cycle_id)
            REFERENCES evaluation_cycles (id);
    END IF;
END $$;