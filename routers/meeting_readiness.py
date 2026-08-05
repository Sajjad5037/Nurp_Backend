from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session, aliased
from sqlalchemy import func

from database import get_db
from models.employee import Employee
from models.evaluation_assignment import EvaluationAssignment

router = APIRouter(
    prefix="/meeting-readiness",
    tags=["Meeting Readiness"]
)


@router.get("")
def get_meeting_readiness(
    db: Session = Depends(get_db)
):

    latest_assignments = (

        db.query(

            func.max(EvaluationAssignment.id).label("latest_id")

        )

        .group_by(

            EvaluationAssignment.employee_id

        )

        .subquery()

    )

    Supervisor = aliased(Employee)

    assignments = (

        db.query(

            EvaluationAssignment,

            Employee.full_name.label("employee_name"),

            Supervisor.full_name.label("supervisor_name")

        )

        .join(

            latest_assignments,

            EvaluationAssignment.id == latest_assignments.c.latest_id

        )

        .join(

            Employee,

            Employee.id == EvaluationAssignment.employee_id

        )

        .join(

            Supervisor,

            Supervisor.id == EvaluationAssignment.supervisor_id

        )

        .order_by(

            Employee.full_name

        )

        .all()

    )

    results = []

    for assignment, employee_name, supervisor_name in assignments:

        employee_completed = (
            assignment.employee_completed_at is not None
        )

        supervisor_completed = (
            assignment.supervisor_completed_at is not None
        )

        hr_completed = (
            assignment.hr_completed_at is not None
        )

        if hr_completed:

            meeting_status = "Ready to Schedule"

        elif supervisor_completed:

            meeting_status = "Waiting on HR"

        elif employee_completed:

            meeting_status = "Waiting on Supervisor"

        else:

            meeting_status = "Waiting on Employee"

        results.append({

            "assignment_id": assignment.id,

            "employee_name": employee_name,

            "supervisor_name": supervisor_name,

            "status": assignment.status,

            "current_stage": assignment.current_stage,

            "employee_completed": employee_completed,

            "supervisor_completed": supervisor_completed,

            "hr_completed": hr_completed,

            "meeting_status": meeting_status

        })

    return results