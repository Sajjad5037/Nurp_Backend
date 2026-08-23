from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database import get_db
from models.evaluation_preview_response import EvaluationPreviewResponse


router = APIRouter(
    prefix="/employee-evaluation",
    tags=["Employee Evaluation Preview"],
)


@router.get("/preview-responses")
def get_preview_responses(
    db: Session = Depends(get_db),
):

    preview_record = (
        db.query(EvaluationPreviewResponse)
        .filter(
            EvaluationPreviewResponse.workflow_id == "form-builder-preview"
        )
        .first()
    )

    if preview_record is None:
        raise HTTPException(
            status_code=404,
            detail="Employee evaluation preview responses not found.",
        )

    preview_responses = preview_record.preview_responses or {}

    return {
        "employee_responses": preview_responses.get("employee_responses", {}),
        "supervisor_responses": preview_responses.get("supervisor_responses", {}),
        "hr_responses": preview_responses.get("hr_responses", {}),
    }
