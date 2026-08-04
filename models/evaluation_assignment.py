from sqlalchemy import (
    Column,
    Integer,
    String,
    ForeignKey,
    DateTime,
    func
)
from sqlalchemy.dialects.postgresql import JSONB

from database import Base


class EvaluationAssignment(Base):

    __tablename__ = "evaluation_assignments"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    template_id = Column(
        Integer,
        ForeignKey("evaluation_templates.id"),
        nullable=False
    )

    employee_id = Column(
        Integer,
        ForeignKey("employees.id"),
        nullable=False
    )

    supervisor_id = Column(
        Integer,
        ForeignKey("employees.id"),
        nullable=False
    )

    hr_id = Column(
        Integer,
        ForeignKey("employees.id"),
        nullable=False
    )

    workflow_json = Column(
        JSONB,
        nullable=False
    )

    current_stage = Column(
        String,
        nullable=False,
        default="employee"
    )

    status = Column(
        String,
        nullable=False,
        default="waiting_for_employee"
    )

    employee_completed_at = Column(
        DateTime(timezone=True),
        nullable=True
    )

    supervisor_completed_at = Column(
        DateTime(timezone=True),
        nullable=True
    )

    hr_completed_at = Column(
        DateTime(timezone=True),
        nullable=True
    )

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False
    )

    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False
    )
    access_token = Column(String, unique=True, nullable=False)

    employee_responses = Column(JSONB, nullable=True)

    supervisor_responses = Column(JSONB, nullable=True)

    hr_responses = Column(JSONB, nullable=True)