from datetime import datetime
from typing import Any

from pydantic import BaseModel


# --------------------------------------------------
# Create Evaluation Assignment
# --------------------------------------------------

class EvaluationAssignmentCreate(BaseModel):

    template_id: int

    employee_id: int

    supervisor_id: int

    hr_id: int


# --------------------------------------------------
# Update Evaluation Assignment
# --------------------------------------------------

class EvaluationAssignmentUpdate(BaseModel):

    current_stage: str

    status: str


# --------------------------------------------------
# Response
# --------------------------------------------------

class EvaluationAssignmentResponse(BaseModel):

    id: int

    template_id: int

    employee_id: int

    supervisor_id: int

    hr_id: int

    workflow_json: dict[str, Any]

    access_token: str

    current_stage: str

    status: str

    employee_completed_at: datetime | None = None

    supervisor_completed_at: datetime | None = None

    hr_completed_at: datetime | None = None

    created_at: datetime

    updated_at: datetime

    class Config:

        from_attributes = True