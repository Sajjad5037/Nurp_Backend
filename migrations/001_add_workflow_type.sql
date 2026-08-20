ALTER TABLE evaluation_assignments
    ADD COLUMN IF NOT EXISTS workflow_type VARCHAR NOT NULL DEFAULT 'goal_kpi_setting';

UPDATE evaluation_assignments
SET workflow_type = CASE
    WHEN workflow_json ->> 'type' = 'employee_evaluation'
        THEN 'employee_evaluation'
    ELSE 'goal_kpi_setting'
END
WHERE workflow_type IS NULL
   OR workflow_type NOT IN ('goal_kpi_setting', 'employee_evaluation');
