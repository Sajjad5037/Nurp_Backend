from datetime import datetime
from pydantic import BaseModel


# --------------------------------------------------
# Create Employee
# --------------------------------------------------

class EmployeeCreate(BaseModel):

    full_name: str

    email: str

    slack_id: str | None = None

    department: str | None = None

    designation: str | None = None

    role: str


# --------------------------------------------------
# Update Employee
# --------------------------------------------------

class EmployeeUpdate(BaseModel):

    full_name: str

    email: str

    slack_id: str | None = None

    department: str | None = None

    designation: str | None = None

    role: str

    is_active: bool = True

    is_existing_employee: bool = False


# --------------------------------------------------
# Employee Response
# --------------------------------------------------

class EmployeeResponse(BaseModel):

    id: int

    full_name: str

    email: str

    slack_id: str | None

    department: str | None

    designation: str | None

    role: str

    is_existing_employee: bool

    is_active: bool

    created_at: datetime

    updated_at: datetime

    class Config:

        from_attributes = True