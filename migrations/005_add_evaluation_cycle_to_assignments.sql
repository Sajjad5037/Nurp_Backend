ALTER TABLE evaluation_assignments
    ADD COLUMN IF NOT EXISTS evaluation_cycle_id INTEGER NULL;

DO $$
BEGIN
    IF NOT EXISTS (
        SELECT 1
        FROM pg_constraint
        WHERE conname = 'fk_evaluation_assignments_evaluation_cycle'
    ) THEN
        ALTER TABLE evaluation_assignments
            ADD CONSTRAINT fk_evaluation_assignments_evaluation_cycle
            FOREIGN KEY (evaluation_cycle_id)
            REFERENCES evaluation_cycles (id);
    END IF;
END $$;

CREATE UNIQUE INDEX IF NOT EXISTS uq_employee_evaluation_assignment_cycle
    ON evaluation_assignments (employee_id, evaluation_cycle_id)
    WHERE workflow_type = 'employee_evaluation';