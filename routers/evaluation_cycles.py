from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from database import get_db
from models.evaluation_cycle import EvaluationCycle
from schemas.evaluation_cycle import (
    EvaluationCycleInvitationUpdate,
    EvaluationCycleResponse,
)
from services.evaluation_cycle_service import ensure_evaluation_cycles

router = APIRouter(
    prefix="/evaluation-cycles",
    tags=["Evaluation Cycles"],
)


@router.get(
    "",
    response_model=list[EvaluationCycleResponse],
)
def get_evaluation_cycles(
    year: int = Query(..., ge=1),
    db: Session = Depends(get_db),
):
    return ensure_evaluation_cycles(db, year)


@router.put(
    "/{cycle_id}",
    response_model=EvaluationCycleResponse,
)
def update_evaluation_cycle(
    cycle_id: int,
    update: EvaluationCycleInvitationUpdate,
    db: Session = Depends(get_db),
):
    cycle = (
        db.query(EvaluationCycle)
        .filter(EvaluationCycle.id == cycle_id)
        .first()
    )

    if not cycle:
        raise HTTPException(
            status_code=404,
            detail="Evaluation cycle not found.",
        )

    cycle.invitation_date = update.invitation_date
    db.commit()
    db.refresh(cycle)

    return cycle