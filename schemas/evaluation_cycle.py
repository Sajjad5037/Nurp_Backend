from datetime import date, datetime

from pydantic import BaseModel


class EvaluationCycleInvitationUpdate(BaseModel):

    invitation_date: date | None = None


class EvaluationCycleResponse(BaseModel):

    id: int
    year: int
    quarter: int
    start_date: date
    end_date: date
    invitation_date: date | None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True