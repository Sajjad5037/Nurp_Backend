ALTER TABLE evaluation_templates
    ADD COLUMN IF NOT EXISTS workflow_type VARCHAR NULL;