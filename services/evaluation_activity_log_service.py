from typing import Any

from sqlalchemy.orm import Session

from models.evaluation_activity_log import EvaluationActivityLog


def log_evaluation_activity(
    db: Session,
    assignment_id: int,
    employee_id: int,
    actor_id: int,
    actor_role: str,
    workflow_type: str,
    stage: str | None = None,
    action: str | None = None,
    component_id: str | None = None,
    component_name: str | None = None,
    details: dict[str, Any] | None = None,
) -> EvaluationActivityLog:
    log = EvaluationActivityLog(
        assignment_id=assignment_id,
        employee_id=employee_id,
        actor_id=actor_id,
        actor_role=actor_role,
        workflow_type=workflow_type,
        stage=stage,
        action=action,
        component_id=component_id,
        component_name=component_name,
        details=details,
    )

    db.add(log)

    return log
