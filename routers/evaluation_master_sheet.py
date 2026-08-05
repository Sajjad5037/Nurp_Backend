from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session, aliased
from sqlalchemy import func

from database import get_db
from models.employee import Employee
from models.evaluation_assignment import EvaluationAssignment

router = APIRouter(
    prefix="/evaluation-master-sheets",
    tags=["Evaluation Master Sheets"]
)


@router.get("/{assignment_id}")
def get_master_sheet(
    assignment_id: int,
    db: Session = Depends(get_db)
):

    assignment = (
        db.query(EvaluationAssignment)
        .filter(EvaluationAssignment.id == assignment_id)
        .first()
    )

    if not assignment:

        raise HTTPException(
            status_code=404,
            detail="Assignment not found."
        )

    employee = (
        db.query(Employee)
        .filter(Employee.id == assignment.employee_id)
        .first()
    )

    supervisor = (
        db.query(Employee)
        .filter(Employee.id == assignment.supervisor_id)
        .first()
    )

    return {

        "id": assignment.id,

        "employee_name": employee.full_name if employee else None,

        "employee_email": employee.email if employee else None,

        "supervisor_name": supervisor.full_name if supervisor else None,

        "supervisor_email": supervisor.email if supervisor else None,

        "current_stage": assignment.current_stage,

        "status": assignment.status,

        "workflow_json": assignment.workflow_json,

        "employee_responses": assignment.employee_responses,

        "supervisor_responses": assignment.supervisor_responses,

        "hr_responses": assignment.hr_responses,

        "employee_completed_at": assignment.employee_completed_at,

        "supervisor_completed_at": assignment.supervisor_completed_at,

        "hr_completed_at": assignment.hr_completed_at

    }
@router.get("")
def get_latest_master_sheets(
    db: Session = Depends(get_db)
):

    latest_assignments = (

        db.query(

            func.max(EvaluationAssignment.id).label("latest_id")

        )

        .filter(

            EvaluationAssignment.status == "completed"

        )

        .group_by(

            EvaluationAssignment.employee_id

        )

        .subquery()

    )

    EmployeeAlias = aliased(Employee)

    assignments = (

        db.query(

            EvaluationAssignment,

            Employee.full_name.label("employee_name"),

            EmployeeAlias.full_name.label("supervisor_name")

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

            EmployeeAlias,

            EmployeeAlias.id == EvaluationAssignment.supervisor_id

        )

        .order_by(

            Employee.full_name

        )

        .all()

    )

    results = []

    for assignment, employee_name, supervisor_name in assignments:

        results.append({

            "assignment_id": assignment.id,

            "employee_name": employee_name,

            "supervisor_name": supervisor_name,

            "status": assignment.status

        })

    return results