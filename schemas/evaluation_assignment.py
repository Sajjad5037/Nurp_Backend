from datetime import datetime
from typing import Any, Dict

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
class EvaluationSubmission(BaseModel):

    responses: dict[str, Any]

# --------------------------------------------------
# Response
# --------------------------------------------------

class EvaluationAssignmentResponse(BaseModel):

    id: int

    template_id: int

    employee_id: int

    supervisor_id: int

    hr_id: int

    workflow_json: Dict[str, Any]

    current_stage: str

    status: str

    employee_completed_at: datetime | None

    supervisor_completed_at: datetime | None

    hr_completed_at: datetime | None

    created_at: datetime

    updated_at: datetime

    class Config:

        from_attributes = True