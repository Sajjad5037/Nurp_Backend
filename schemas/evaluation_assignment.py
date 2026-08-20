from datetime import datetime
from typing import Any, Dict

from pydantic import BaseModel
from uuid import UUID

# --------------------------------------------------
# Create Evaluation Assignment
# --------------------------------------------------

class EvaluationAssignmentCreate(BaseModel):

    template_id: int

    employee_id: int

    supervisor_id: int

    hr_id: int

    workflow_type: str | None = None

    evaluation_cycle_id: int | None = None


# --------------------------------------------------
# Update Evaluation Assignment
# --------------------------------------------------

class EvaluationAssignmentUpdate(BaseModel):

    current_stage: str

    status: str
class EvaluationSubmission(BaseModel):

    responses: dict[str, Any]
class EvaluationAssignmentLinkResponse(BaseModel):

    id: int

    assignment_id: int

    stage: str

    access_token: UUID

    email: str | None

    created_at: datetime

    opened_at: datetime | None

    completed_at: datetime | None

    expires_at: datetime | None

    class Config:

        from_attributes = True
# --------------------------------------------------
# Response
# --------------------------------------------------

class EvaluationAssignmentResponse(BaseModel):

    id: int

    template_id: int

    employee_id: int

    supervisor_id: int

    hr_id: int

    evaluation_cycle_id: int | None

    workflow_json: Dict[str, Any]

    workflow_type: str

    current_stage: str

    status: str

    employee_completed_at: datetime | None

    supervisor_completed_at: datetime | None

    hr_completed_at: datetime | None

    created_at: datetime

    updated_at: datetime

    class Config:

        from_attributes = True