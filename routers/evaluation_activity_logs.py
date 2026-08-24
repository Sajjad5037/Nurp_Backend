from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session, aliased

from database import get_db
from models.employee import Employee
from models.evaluation_activity_log import EvaluationActivityLog

router = APIRouter(
    prefix="/evaluation-activity-logs",
    tags=["Evaluation Activity Logs"]
)


@router.get("")
def get_evaluation_activity_logs(
    db: Session = Depends(get_db)
):

    EmployeeRecord = aliased(Employee)
    ActorRecord = aliased(Employee)

    activities = (
        db.query(
            EvaluationActivityLog,
            EmployeeRecord.full_name.label("employee_name"),
            ActorRecord.full_name.label("actor_name")
        )
        .outerjoin(
            EmployeeRecord,
            EmployeeRecord.id == EvaluationActivityLog.employee_id
        )
        .outerjoin(
            ActorRecord,
            ActorRecord.id == EvaluationActivityLog.actor_id
        )
        .order_by(EvaluationActivityLog.created_at.desc())
        .all()
    )

    return [
        {
            "id": activity.id,
            "assignment_id": activity.assignment_id,
            "employee_id": activity.employee_id,
            "actor_id": activity.actor_id,
            "actor_role": activity.actor_role,
            "workflow_type": activity.workflow_type,
            "stage": activity.stage,
            "action": activity.action,
            "component_id": activity.component_id,
            "component_name": activity.component_name,
            "details": activity.details,
            "created_at": activity.created_at,
            "employee_name": employee_name,
            "actor_name": actor_name
        }
        for activity, employee_name, actor_name in activities
    ]
