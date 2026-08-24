from calendar import month_name
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from database import get_db
from datetime import datetime, timezone

from models.employee import Employee
from models.evaluation_template import EvaluationTemplate
from models.evaluation_assignment import EvaluationAssignment
from models.evaluation_cycle import EvaluationCycle
from models.finalized_goal import FinalizedGoal
from models.finalized_kpi import FinalizedKPI
from services.evaluation_cycle_service import get_current_evaluation_cycle
from services.finalized_target_service import extract_finalized_targets
from services.evaluation_activity_log_service import log_evaluation_activity
import uuid
from models.evaluation_assignment_link import EvaluationAssignmentLink


from models.evaluation_assignment_link import EvaluationAssignmentLink
from utils.email_service import (
    send_employee_evaluation_email,
    send_supervisor_evaluation_email,
    send_hr_evaluation_email
)
from schemas.evaluation_assignment import (
    EvaluationAssignmentCreate,
    EvaluationAssignmentResponse,
    EvaluationSubmission
)

router = APIRouter(
    prefix="/evaluation-assignments",
    tags=["Evaluation Assignments"]
)

WORKFLOW_TYPES = {
    "goal_kpi_setting",
    "employee_evaluation",
}


def resolve_workflow_type(
    requested_type,
    workflow_json
):

    workflow_type = (
        requested_type or
        workflow_json.get("type") or
        "goal_kpi_setting"
    )

    if workflow_type not in WORKFLOW_TYPES:

        raise HTTPException(
            status_code=400,
            detail="Invalid workflow type."
        )

    return workflow_type


# --------------------------------------------------
# Create Evaluation Assignment
# --------------------------------------------------

@router.post(
    "",
    response_model=EvaluationAssignmentResponse
)
def create_assignment(
    assignment: EvaluationAssignmentCreate,
    db: Session = Depends(get_db)
):

    print("==============================================")
    print("CREATE EVALUATION ASSIGNMENT DEBUG")
    print("==============================================")
    print("employee_id:", assignment.employee_id)
    print("supervisor_id:", assignment.supervisor_id)
    print("hr_id:", assignment.hr_id)
    print("template_id:", assignment.template_id)
    print("requested workflow_type:", assignment.workflow_type)
    print("evaluation_cycle_id:", assignment.evaluation_cycle_id)

    # -----------------------------------------------
    # Validate Employee
    # -----------------------------------------------

    employee = (
        db.query(Employee)
        .filter(Employee.id == assignment.employee_id)
        .first()
    )

    print("Employee found:", employee.id if employee else None)
    print("Employee name:", employee.full_name if employee else None)

    if not employee:
        raise HTTPException(
            status_code=404,
            detail="Employee not found."
        )

    # -----------------------------------------------
    # Validate Supervisor
    # -----------------------------------------------

    supervisor = (
        db.query(Employee)
        .filter(Employee.id == assignment.supervisor_id)
        .first()
    )

    print("Supervisor found:", supervisor.id if supervisor else None)
    print("Supervisor name:", supervisor.full_name if supervisor else None)

    if not supervisor:
        raise HTTPException(
            status_code=404,
            detail="Supervisor not found."
        )

    # -----------------------------------------------
    # Validate HR
    # -----------------------------------------------

    hr = (
        db.query(Employee)
        .filter(Employee.id == assignment.hr_id)
        .first()
    )

    print("HR found:", hr.id if hr else None)
    print("HR name:", hr.full_name if hr else None)

    if not hr:
        raise HTTPException(
            status_code=404,
            detail="HR employee not found."
        )

    # -----------------------------------------------
    # Load Template
    # -----------------------------------------------

    template = (
        db.query(EvaluationTemplate)
        .filter(EvaluationTemplate.id == assignment.template_id)
        .first()
    )

    print("----------------------------------------------")
    print("TEMPLATE DEBUG")
    print("Template found:", template.id if template else None)
    print("Template name:", template.name if template else None)
    print("Template workflow_type:", template.workflow_type if template else None)
    print("Template status:", template.status if template else None)

    if not template:
        raise HTTPException(
            status_code=404,
            detail="Evaluation template not found."
        )

    print("----------------------------------------------")
    print("WORKFLOW TYPE RESOLUTION")
    print("Requested workflow type:", assignment.workflow_type)
    print(
        "Workflow JSON type:",
        template.workflow_json.get("type")
        if template and template.workflow_json
        else None
    )

    workflow_type = resolve_workflow_type(
        assignment.workflow_type or template.workflow_type,
        template.workflow_json
    )

    print("Resolved workflow type:", workflow_type)

    evaluation_cycle = None

    if workflow_type == "employee_evaluation":

        if assignment.evaluation_cycle_id is None:
            evaluation_cycle = get_current_evaluation_cycle(db)
        else:
            evaluation_cycle = (
                db.query(EvaluationCycle)
                .filter(EvaluationCycle.id == assignment.evaluation_cycle_id)
                .first()
            )

        print("----------------------------------------------")
        print("EMPLOYEE EVALUATION CYCLE")
        print(
            "Evaluation cycle:",
            evaluation_cycle.id if evaluation_cycle else None
        )

        if not evaluation_cycle:
            raise HTTPException(
                status_code=400,
                detail=(
                    "No evaluation cycle is available for "
                    "this employee evaluation assignment."
                )
            )

        duplicate_assignment = (
            db.query(EvaluationAssignment)
            .filter(
                EvaluationAssignment.employee_id == assignment.employee_id,
                EvaluationAssignment.evaluation_cycle_id == evaluation_cycle.id,
                EvaluationAssignment.workflow_type == "employee_evaluation"
            )
            .first()
        )

        if duplicate_assignment:
            raise HTTPException(
                status_code=409,
                detail=(
                    "An Employee Evaluation already exists for this "
                    "employee and Evaluation Cycle."
                )
            )

    elif workflow_type == "goal_kpi_setting":

        evaluation_cycle = get_current_evaluation_cycle(db)

        print("----------------------------------------------")
        print("GOAL/KPI EVALUATION CYCLE")
        print(
            "Current evaluation cycle:",
            evaluation_cycle.id if evaluation_cycle else None
        )

    # -----------------------------------------------
    # Create Assignment
    # -----------------------------------------------

    print("----------------------------------------------")
    print("ABOUT TO CREATE ASSIGNMENT")
    print("workflow_type:", workflow_type)
    print("evaluation_cycle_id:", evaluation_cycle.id if evaluation_cycle else None)
    print("template_id:", template.id if template else None)

    access_token = str(uuid.uuid4())

    db_assignment = EvaluationAssignment(

        template_id=assignment.template_id,

        employee_id=assignment.employee_id,

        supervisor_id=assignment.supervisor_id,

        hr_id=assignment.hr_id,

        workflow_json=template.workflow_json,

        workflow_type=workflow_type,

        evaluation_cycle_id=(
            evaluation_cycle.id if evaluation_cycle else None
        ),

        access_token=access_token,

        current_stage="employee",

        status="waiting_for_employee"

    )

    db.add(db_assignment)

    try:
        db.commit()
    except IntegrityError as error:
        db.rollback()

        if "uq_employee_evaluation_assignment_cycle" in str(error.orig):
            raise HTTPException(
                status_code=409,
                detail=(
                    "An Employee Evaluation already exists for this "
                    "employee and Evaluation Cycle."
                )
            )

        raise

    db.refresh(db_assignment)
    # -----------------------------------------------
    # Create Stage Access Links
    # -----------------------------------------------

    employee_link = EvaluationAssignmentLink(

        assignment_id=db_assignment.id,

        stage="employee",

        access_token=uuid.uuid4(),

        email=employee.email

    )

    supervisor_link = EvaluationAssignmentLink(

        assignment_id=db_assignment.id,

        stage="supervisor",

        access_token=uuid.uuid4(),

        email=supervisor.email

    )

    hr_link = EvaluationAssignmentLink(

        assignment_id=db_assignment.id,

        stage="hr",

        access_token=uuid.uuid4(),

        email=hr.email

    )

    db.add(employee_link)

    db.add(supervisor_link)

    db.add(hr_link)

    db.commit()
    db.commit()

    send_employee_evaluation_email(

        employee_name=employee.full_name,

        employee_email=employee.email,

        access_token=str(employee_link.access_token)

    )

    if workflow_type == "employee_evaluation":

        send_supervisor_evaluation_email(

            supervisor_name=supervisor.full_name,

            supervisor_email=supervisor.email,

            employee_name=employee.full_name,

            access_token=str(supervisor_link.access_token)

        )

        send_hr_evaluation_email(

            hr_name=hr.full_name,

            hr_email=hr.email,

            employee_name=employee.full_name,

            access_token=str(hr_link.access_token)

        )

    print("----------------------------------------------")
    print("ASSIGNMENT CREATED SUCCESSFULLY")
    print("assignment id:", db_assignment.id)
    print("==============================================")

    return db_assignment


# --------------------------------------------------
# Get All Assignments
# --------------------------------------------------

@router.get(
    "",
    response_model=list[EvaluationAssignmentResponse]
)
def get_assignments(
    db: Session = Depends(get_db)
):

    return (
        db.query(EvaluationAssignment)
        .order_by(EvaluationAssignment.created_at.desc())
        .all()
    )

# --------------------------------------------------
# Get Assignment By Access Token
# --------------------------------------------------

@router.get("/token/{access_token}")
def get_assignment_by_token(
    access_token: str,
    db: Session = Depends(get_db)
):

    # -----------------------------------------------
    # Find Access Link
    # -----------------------------------------------

    link = (
        db.query(EvaluationAssignmentLink)
        .filter(
            EvaluationAssignmentLink.access_token == access_token
        )
        .first()
    )

    if not link:

        raise HTTPException(
            status_code=404,
            detail="Invalid or expired evaluation link."
        )
    # -----------------------------------------------
    # Prevent Reusing Completed Links
    # -----------------------------------------------

    if link.completed_at is not None:

        raise HTTPException(
            status_code=403,
            detail="This evaluation has already been submitted."
        )
    # -----------------------------------------------
    # Record First Open
    # -----------------------------------------------

    if link.opened_at is None:

        link.opened_at = datetime.utcnow()

        db.commit()

    # -----------------------------------------------
    # Load Assignment
    # -----------------------------------------------

    assignment = (
        db.query(EvaluationAssignment)
        .filter(
            EvaluationAssignment.id == link.assignment_id
        )
        .first()
    )

    if not assignment:

        raise HTTPException(
            status_code=404,
            detail="Evaluation assignment not found."
        )

    employee = (
        db.query(Employee)
        .filter(Employee.id == assignment.employee_id)
        .first()
    )

    if not employee:

        raise HTTPException(
            status_code=404,
            detail="Employee not found."
        )

    supervisor = (
        db.query(Employee)
        .filter(Employee.id == assignment.supervisor_id)
        .first()
    )

    review_cycle = None
    review_cycle_months = None
    finalized_goals = []
    finalized_kpis = []

    if assignment.evaluation_cycle_id is not None:

        cycle = (
            db.query(EvaluationCycle)
            .filter(
                EvaluationCycle.id == assignment.evaluation_cycle_id
            )
            .first()
        )

        if cycle:
            review_cycle = (
                f"Q{cycle.quarter} {cycle.year} "
                f"({cycle.start_date.strftime('%b')} "
                f"– {cycle.end_date.strftime('%b')})"
            )
            review_cycle_months = [
                month_name[month]
                for month in range(
                    cycle.start_date.month,
                    cycle.end_date.month + 1,
                )
            ]

    if (
        assignment.workflow_type == "employee_evaluation"
        and assignment.evaluation_cycle_id is not None
    ):
        finalized_goals = (
            db.query(FinalizedGoal)
            .filter(
                FinalizedGoal.employee_id == assignment.employee_id,
                FinalizedGoal.evaluation_cycle_id == assignment.evaluation_cycle_id,
            )
            .order_by(FinalizedGoal.sequence.asc())
            .all()
        )
        finalized_kpis = (
            db.query(FinalizedKPI)
            .join(
                EvaluationAssignment,
                FinalizedKPI.source_assignment_id == EvaluationAssignment.id,
            )
            .filter(
                FinalizedKPI.employee_id == assignment.employee_id,
                EvaluationAssignment.employee_id == assignment.employee_id,
                EvaluationAssignment.evaluation_cycle_id == assignment.evaluation_cycle_id,
                EvaluationAssignment.workflow_type == "goal_kpi_setting",
            )
            .order_by(FinalizedKPI.sequence.asc())
            .all()
        )

    print("======================================")
    print("Evaluation Assignment:", assignment.id)
    print("Current Stage:", assignment.current_stage)
    print("--------------------------------------")
    print("Employee Responses:")
    print(assignment.employee_responses)
    print("--------------------------------------")
    print("Supervisor Responses:")
    print(assignment.supervisor_responses)
    print("--------------------------------------")
    print("HR Responses:")
    print(assignment.hr_responses)
    print("======================================")

    return {

        "id": assignment.id,

        "employee_name": employee.full_name,

        "employee_email": employee.email,

        "supervisor_name": (
            supervisor.full_name if supervisor else None
        ),

        "department": employee.department,

        "designation": employee.designation,

        "review_cycle": review_cycle,

        "review_cycle_months": review_cycle_months,

        "finalized_goals": [
            {
                "id": goal.id,
                "sequence": goal.sequence,
                "description": goal.description,
            }
            for goal in finalized_goals
        ],

        "finalized_kpis": [
            {
                "id": kpi.id,
                "sequence": kpi.sequence,
                "title": kpi.title,
                "expectation": kpi.expectation,
            }
            for kpi in finalized_kpis
        ],

        "current_stage": assignment.current_stage,

        "access_stage": link.stage,

        "status": assignment.status,

        "workflow_json": assignment.workflow_json,

        "employee_responses": assignment.employee_responses,

        "supervisor_responses": assignment.supervisor_responses,

        "hr_responses": assignment.hr_responses

    }
# --------------------------------------------------
# Employee Submit Evaluation
# --------------------------------------------------

@router.post("/{assignment_id}/submit")
def submit_evaluation(

    assignment_id: int,

    submission: EvaluationSubmission,

    access_stage: str | None = None,

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

            detail="Evaluation assignment not found."

        )

    # ------------------------------------------
    # Independent Employee Evaluation Workflow
    # ------------------------------------------

    if assignment.workflow_type == "employee_evaluation":

        if access_stage not in {
            "employee",
            "supervisor",
            "hr"
        }:

            raise HTTPException(

                status_code=400,

                detail=(
                    "A valid access_stage is required for "
                    "employee_evaluation submissions."
                )

            )

        if access_stage == "employee":

            print("DEBUG EMPLOYEE SUBMISSION RESPONSES:")
            print(submission.responses)

            assignment.employee_responses = submission.responses

            assignment.employee_completed_at = datetime.now(
                timezone.utc
            )

            log_evaluation_activity(
                db=db,
                assignment_id=assignment.id,
                employee_id=assignment.employee_id,
                actor_id=assignment.employee_id,
                actor_role="employee",
                workflow_type=assignment.workflow_type,
                stage="employee",
                action="submitted",
                details={
                    "status": "submitted"
                }
            )

            assignment.current_stage = "supervisor"
            assignment.status = "waiting_for_supervisor"

            employee_link = (
                db.query(EvaluationAssignmentLink)
                .filter(
                    EvaluationAssignmentLink.assignment_id == assignment.id,
                    EvaluationAssignmentLink.stage == "employee"
                )
                .first()
            )

            if employee_link:

                employee_link.completed_at = datetime.now(timezone.utc)

        elif access_stage == "supervisor":

            assignment.supervisor_responses = submission.responses

            log_evaluation_activity(
                db=db,
                assignment_id=assignment.id,
                employee_id=assignment.employee_id,
                actor_id=assignment.supervisor_id,
                actor_role="supervisor",
                workflow_type=assignment.workflow_type,
                stage="supervisor",
                action="submitted",
                details={
                    "status": "submitted"
                }
            )

            assignment.supervisor_completed_at = datetime.now(
                timezone.utc
            )

            assignment.current_stage = "hr"
            assignment.status = "waiting_for_hr"

            supervisor_link = (
                db.query(EvaluationAssignmentLink)
                .filter(
                    EvaluationAssignmentLink.assignment_id == assignment.id,
                    EvaluationAssignmentLink.stage == "supervisor"
                )
                .first()
            )

            if supervisor_link:

                supervisor_link.completed_at = datetime.now(timezone.utc)

        elif access_stage == "hr":

            assignment.hr_responses = submission.responses

            # HR can remove employee-submitted extra projects.
            # Preserve all other employee response data unchanged.
            updated_employee_projects = (
                submission.responses.get("extra_projects")
            )

            if updated_employee_projects is not None:

                employee_responses = (
                    assignment.employee_responses or {}
                ).copy()

                employee_responses["extra_projects"] = (
                    updated_employee_projects
                )

                assignment.employee_responses = (
                    employee_responses
                )

            assignment.hr_completed_at = datetime.now(
                timezone.utc
            )

            log_evaluation_activity(
                db=db,
                assignment_id=assignment.id,
                employee_id=assignment.employee_id,
                actor_id=assignment.hr_id,
                actor_role="hr",
                workflow_type=assignment.workflow_type,
                stage="hr",
                action="submitted",
                details={
                    "status": "completed"
                }
            )

            assignment.current_stage = "completed"
            assignment.status = "completed"

            hr_link = (
                db.query(EvaluationAssignmentLink)
                .filter(
                    EvaluationAssignmentLink.assignment_id == assignment.id,
                    EvaluationAssignmentLink.stage == "hr"
                )
                .first()
            )

            if hr_link:

                hr_link.completed_at = datetime.now(timezone.utc)

        db.commit()

        db.refresh(assignment)

        return {

            "message": "Evaluation saved successfully.",

            "current_stage": assignment.current_stage,

            "status": assignment.status,

            "access_stage": access_stage

        }

    # ------------------------------------------
    # Employee Submission
    # ------------------------------------------

    if assignment.current_stage == "employee":

        print("DEBUG EMPLOYEE SUBMISSION RESPONSES:")
        print(submission.responses)

        assignment.employee_responses = submission.responses

        if assignment.workflow_type == "goal_kpi_setting":

            log_evaluation_activity(
                db=db,
                assignment_id=assignment.id,
                employee_id=assignment.employee_id,
                actor_id=assignment.employee_id,
                actor_role="employee",
                workflow_type=assignment.workflow_type,
                stage="employee",
                action="submitted",
                details={
                    "status": "submitted"
                }
            )

        assignment.employee_completed_at = datetime.now(
            timezone.utc
        )

        assignment.current_stage = "supervisor"

        assignment.status = "waiting_for_supervisor"

        employee_link = (
            db.query(EvaluationAssignmentLink)
            .filter(
                EvaluationAssignmentLink.assignment_id == assignment.id,
                EvaluationAssignmentLink.stage == "employee"
            )
            .first()
        )

        if employee_link:

            employee_link.completed_at = datetime.now(timezone.utc)

        db.commit()

        db.refresh(assignment)

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

        supervisor_link = (
            db.query(EvaluationAssignmentLink)
            .filter(
                EvaluationAssignmentLink.assignment_id == assignment.id,
                EvaluationAssignmentLink.stage == "supervisor"
            )
            .first()
        )

        send_supervisor_evaluation_email(

            supervisor_name=supervisor.full_name,

            supervisor_email=supervisor.email,

            employee_name=employee.full_name,

            access_token=str(supervisor_link.access_token)

        )

    # ------------------------------------------
    # Supervisor Submission
    # ------------------------------------------

    elif assignment.current_stage == "supervisor":

        print("====================================")
        print("SUPERVISOR SUBMISSION RECEIVED")
        print("submission.responses:")
        print(submission.responses)

        assignment.supervisor_responses = submission.responses

        if assignment.workflow_type == "goal_kpi_setting":

            log_evaluation_activity(
                db=db,
                assignment_id=assignment.id,
                employee_id=assignment.employee_id,
                actor_id=assignment.supervisor_id,
                actor_role="supervisor",
                workflow_type=assignment.workflow_type,
                stage="supervisor",
                action="submitted",
                details={
                    "status": "submitted"
                }
            )

        print("------------------------------------")
        print("assignment.supervisor_responses BEFORE COMMIT:")
        print(assignment.supervisor_responses)

        assignment.supervisor_completed_at = datetime.now(
            timezone.utc
        )

        assignment.current_stage = "hr"

        assignment.status = "waiting_for_hr"

        supervisor_link = (
            db.query(EvaluationAssignmentLink)
            .filter(
                EvaluationAssignmentLink.assignment_id == assignment.id,
                EvaluationAssignmentLink.stage == "supervisor"
            )
            .first()
        )

        if supervisor_link:

            supervisor_link.completed_at = datetime.now(timezone.utc)

        db.commit()

        db.refresh(assignment)

        print("------------------------------------")
        print("assignment.supervisor_responses AFTER COMMIT:")
        print(assignment.supervisor_responses)
        print("====================================")

        employee = (
            db.query(Employee)
            .filter(Employee.id == assignment.employee_id)
            .first()
        )

        hr = (
            db.query(Employee)
            .filter(Employee.id == assignment.hr_id)
            .first()
        )

        hr_link = (
            db.query(EvaluationAssignmentLink)
            .filter(
                EvaluationAssignmentLink.assignment_id == assignment.id,
                EvaluationAssignmentLink.stage == "hr"
            )
            .first()
        )

        send_hr_evaluation_email(

            hr_name=hr.full_name,

            hr_email=hr.email,

            employee_name=employee.full_name,

            access_token=str(hr_link.access_token)

        )
    elif assignment.current_stage == "hr":

        assignment.hr_responses = submission.responses

        if assignment.workflow_type == "goal_kpi_setting":

            log_evaluation_activity(
                db=db,
                assignment_id=assignment.id,
                employee_id=assignment.employee_id,
                actor_id=assignment.hr_id,
                actor_role="hr",
                workflow_type=assignment.workflow_type,
                stage="hr",
                action="submitted",
                details={
                    "status": "completed"
                }
            )

        assignment.hr_completed_at = datetime.now(
            timezone.utc
        )

        assignment.current_stage = "completed"

        assignment.status = "completed"

        hr_link = (
            db.query(EvaluationAssignmentLink)
            .filter(
                EvaluationAssignmentLink.assignment_id == assignment.id,
                EvaluationAssignmentLink.stage == "hr"
            )
            .first()
        )

        if hr_link:

            hr_link.completed_at = datetime.now(timezone.utc)

        if assignment.workflow_type == "goal_kpi_setting":
            employee = (
                db.query(Employee)
                .filter(Employee.id == assignment.employee_id)
                .first()
            )

            if employee:
                employee.is_existing_employee = True

        db.commit()

        db.refresh(assignment)

        extract_finalized_targets(db, assignment.id)
    else:

        raise HTTPException(

            status_code=400,

            detail="Evaluation is already completed or in an invalid stage."

        )

    return {

        "message": "Evaluation submitted successfully.",

        "current_stage": assignment.current_stage,

        "status": assignment.status

    }
# --------------------------------------------------
# Get Assignment
# --------------------------------------------------

@router.get(
    "/{assignment_id}",
    response_model=EvaluationAssignmentResponse
)
def get_assignment(
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

    return assignment