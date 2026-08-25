-- Allow the same email to be used across different employee roles,
-- while preventing duplicate (email, role) pairs.

DROP INDEX IF EXISTS ix_employees_email;

DO $$
BEGIN
    IF EXISTS (
        SELECT 1
        FROM pg_constraint
        WHERE conname = 'employees_email_key'
    ) THEN
        ALTER TABLE employees
            DROP CONSTRAINT employees_email_key;
    END IF;
END $$;

CREATE INDEX IF NOT EXISTS ix_employees_email
    ON employees (email);

DO $$
BEGIN
    IF NOT EXISTS (
        SELECT 1
        FROM pg_constraint
        WHERE conname = 'uq_employees_email_role'
    ) THEN
        ALTER TABLE employees
            ADD CONSTRAINT uq_employees_email_role
            UNIQUE (email, role);
    END IF;
END $$;
