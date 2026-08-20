DO $$
BEGIN
    IF NOT EXISTS (
        SELECT 1
        FROM pg_constraint
        WHERE conname = 'uq_finalized_goals_source_assignment_sequence'
    ) THEN
        ALTER TABLE finalized_goals
            ADD CONSTRAINT uq_finalized_goals_source_assignment_sequence
            UNIQUE (source_assignment_id, sequence);
    END IF;

    IF NOT EXISTS (
        SELECT 1
        FROM pg_constraint
        WHERE conname = 'uq_finalized_kpis_source_assignment_sequence'
    ) THEN
        ALTER TABLE finalized_kpis
            ADD CONSTRAINT uq_finalized_kpis_source_assignment_sequence
            UNIQUE (source_assignment_id, sequence);
    END IF;
END $$;
