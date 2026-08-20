from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database import get_db
from models.evaluation_template import EvaluationTemplate
from schemas.evaluation_template import (
    EvaluationTemplateCreate,
    EvaluationTemplateUpdate,
    EvaluationTemplateResponse,
)

router = APIRouter(
    prefix="/evaluation-templates",
    tags=["Evaluation Templates"]
)


# ------------------------------------------------------------------
# CREATE
# ------------------------------------------------------------------

@router.post(
    "",
    response_model=EvaluationTemplateResponse
)
def create_template(
    template: EvaluationTemplateCreate,
    db: Session = Depends(get_db)
):

    print("========== CREATE TEMPLATE ==========")
    print("Name:", template.name)

    new_template = EvaluationTemplate(

        name=template.name,

        workflow_json=template.workflow_json,

        workflow_type=template.workflow_type,

        status="draft"

    )

    db.add(new_template)

    print("Added to session")

    db.commit()

    print("Committed")

    db.refresh(new_template)

    print("New ID:", new_template.id)

    return new_template


# ------------------------------------------------------------------
# GET ALL
# ------------------------------------------------------------------

@router.get(
    "",
    response_model=list[EvaluationTemplateResponse]
)
def get_templates(
    db: Session = Depends(get_db)
):

    return db.query(EvaluationTemplate).order_by(
        EvaluationTemplate.created_at.desc()
    ).all()


# ------------------------------------------------------------------
# GET ONE
# ------------------------------------------------------------------

@router.get(
    "/{template_id}",
    response_model=EvaluationTemplateResponse
)
def get_template(
    template_id: int,
    db: Session = Depends(get_db)
):

    template = db.query(EvaluationTemplate).filter(

        EvaluationTemplate.id == template_id

    ).first()

    if not template:

        raise HTTPException(

            status_code=404,

            detail="Template not found."

        )

    return template


# ------------------------------------------------------------------
# UPDATE
# ------------------------------------------------------------------

@router.put(
    "/{template_id}",
    response_model=EvaluationTemplateResponse
)
def update_template(
    template_id: int,
    updated: EvaluationTemplateUpdate,
    db: Session = Depends(get_db)
):

    template = db.query(EvaluationTemplate).filter(

        EvaluationTemplate.id == template_id

    ).first()

    if not template:

        raise HTTPException(

            status_code=404,

            detail="Template not found."

        )

    template.name = updated.name

    template.workflow_json = updated.workflow_json

    template.workflow_type = updated.workflow_type

    db.commit()

    db.refresh(template)

    return template