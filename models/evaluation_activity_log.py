from sqlalchemy import (
    Column,
    DateTime,
    Index,
    Integer,
    String,
    func,
)
from sqlalchemy.dialects.postgresql import JSONB

from database import Base


class EvaluationActivityLog(Base):

    __tablename__ = "evaluation_activity_logs"

    id = Column(
        Integer,
        primary_key=True,
    )

    assignment_id = Column(
        Integer,
        nullable=False,
    )

    employee_id = Column(
        Integer,
        nullable=False,
    )

    actor_id = Column(
        Integer,
        nullable=False,
    )

    actor_role = Column(
        String,
        nullable=False,
    )

    workflow_type = Column(
        String,
        nullable=False,
    )

    stage = Column(
        String,
        nullable=True,
    )

    action = Column(
        String,
        nullable=False,
    )

    component_id = Column(
        String,
        nullable=True,
    )

    component_name = Column(
        String,
        nullable=True,
    )

    details = Column(
        JSONB,
        nullable=True,
    )

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )

    __table_args__ = (
        Index(
            "ix_evaluation_activity_logs_assignment_id",
            "assignment_id",
        ),
        Index(
            "ix_evaluation_activity_logs_employee_id",
            "employee_id",
        ),
        Index(
            "ix_evaluation_activity_logs_actor_id",
            "actor_id",
        ),
        Index(
            "ix_evaluation_activity_logs_workflow_type",
            "workflow_type",
        ),
        Index(
            "ix_evaluation_activity_logs_created_at",
            "created_at",
        ),
    )
