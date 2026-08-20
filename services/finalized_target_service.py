import re

from sqlalchemy.orm import Session

from models.employee import Employee
from models.evaluation_assignment import EvaluationAssignment
from models.evaluation_template import EvaluationTemplate
from models.finalized_goal import FinalizedGoal
from models.finalized_kpi import FinalizedKPI


_ENTRY_KEY_PATTERN = re.compile(r"^(?:goal|kpi)_(\d+)$")


def _ordered_entries(response_data, prefix):

    if not isinstance(response_data, dict):
        return []

    entries = []

    for key, value in response_data.items():

        match = _ENTRY_KEY_PATTERN.fullmatch(key)

        if not match or not key.startswith(prefix + "_"):
            continue

        entries.append((int(match.group(1)), value))

    return sorted(entries, key=lambda item: item[0])


def extract_finalized_targets(
    db: Session,
    assignment_id: int,
):

    assignment = (
        db.query(EvaluationAssignment)
        .filter(EvaluationAssignment.id == assignment_id)
        .first()
    )

    if not assignment:
        raise ValueError("Evaluation assignment not found.")

    if assignment.workflow_type != "goal_kpi_setting":
        raise ValueError(
            "Only goal_kpi_setting assignments can be finalized."
        )

    if assignment.status != "completed":
        raise ValueError(
            "The evaluation assignment must be completed."
        )

    if not assignment.hr_completed_at:
        raise ValueError(
            "The completed assignment has no HR completion timestamp."
        )

    existing_goals = (
        db.query(FinalizedGoal)
        .filter(
            FinalizedGoal.source_assignment_id == assignment.id
        )
        .order_by(FinalizedGoal.sequence)
        .all()
    )

    existing_kpis = (
        db.query(FinalizedKPI)
        .filter(
            FinalizedKPI.source_assignment_id == assignment.id
        )
        .order_by(FinalizedKPI.sequence)
        .all()
    )

    if existing_goals or existing_kpis:

        if not existing_goals or not existing_kpis:
            raise ValueError(
                "Finalized target extraction is partially complete."
            )

        return {
            "created": False,
            "assignment_id": assignment.id,
            "employee_id": assignment.employee_id,
            "goals": existing_goals,
            "kpis": existing_kpis,
        }

    hr_responses = assignment.hr_responses or {}
    goal_responses = hr_responses.get("goal_list", {})
    kpi_responses = hr_responses.get("kpi_list", {})

    finalized_goals = []

    for sequence, response in _ordered_entries(
        goal_responses,
        "goal",
    ):

        if not isinstance(response, dict):
            continue

        description = response.get("final_goal")

        if not isinstance(description, str) or not description.strip():
            continue

        finalized_goals.append(
            FinalizedGoal(
                source_assignment_id=assignment.id,
                employee_id=assignment.employee_id,
                evaluation_cycle_id=assignment.evaluation_cycle_id,
                sequence=sequence,
                title=None,
                description=description.strip(),
                expectation=None,
                success_criteria=None,
                target_date=None,
                weight=None,
                finalized_at=assignment.hr_completed_at,
            )
        )

    finalized_kpis = []

    for sequence, response in _ordered_entries(
        kpi_responses,
        "kpi",
    ):

        if not isinstance(response, dict):
            continue

        title = response.get("title")
        expectation = response.get("expectation")

        if not isinstance(title, str) or not title.strip():
            continue

        if not isinstance(expectation, str) or not expectation.strip():
            continue

        finalized_kpis.append(
            FinalizedKPI(
                source_assignment_id=assignment.id,
                employee_id=assignment.employee_id,
                sequence=sequence,
                title=title.strip(),
                expectation=expectation.strip(),
                finalized_at=assignment.hr_completed_at,
            )
        )

    if not finalized_goals:
        raise ValueError(
            "No HR-finalized goals were found in the assignment."
        )

    if not finalized_kpis:
        raise ValueError(
            "No HR-finalized KPIs were found in the assignment."
        )

    try:

        db.add_all(finalized_goals)
        db.add_all(finalized_kpis)
        db.commit()

    except Exception:

        db.rollback()
        raise

    return {
        "created": True,
        "assignment_id": assignment.id,
        "employee_id": assignment.employee_id,
        "goals": finalized_goals,
        "kpis": finalized_kpis,
    }
