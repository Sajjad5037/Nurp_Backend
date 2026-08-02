from pydantic import BaseModel
from typing import Dict, Any
from datetime import datetime


# ------------------------------------------------------------------
# Request Schema
# ------------------------------------------------------------------

class EvaluationTemplateCreate(BaseModel):

    name: str

    workflow_json: Dict[str, Any]


# ------------------------------------------------------------------
# Update Schema
# ------------------------------------------------------------------

class EvaluationTemplateUpdate(BaseModel):

    name: str

    workflow_json: Dict[str, Any]


# ------------------------------------------------------------------
# Response Schema
# ------------------------------------------------------------------

class EvaluationTemplateResponse(BaseModel):

    id: int

    name: str

    status: str

    workflow_json: Dict[str, Any]

    created_at: datetime

    updated_at: datetime

    class Config:

        from_attributes = True