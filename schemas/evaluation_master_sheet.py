from pydantic import BaseModel


class EvaluationMasterSheetSummary(BaseModel):
    assignment_id: int
    employee_name: str
    supervisor_name: str
    status: str