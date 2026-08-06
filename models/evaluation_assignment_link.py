from sqlalchemy import (
    Column,
    Integer,
    String,
    DateTime,
    ForeignKey,
    func
)
from sqlalchemy.dialects.postgresql import UUID
from database import Base


class EvaluationAssignmentLink(Base):

    __tablename__ = "evaluation_assignment_links"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    assignment_id = Column(
        Integer,
        ForeignKey("evaluation_assignments.id", ondelete="CASCADE"),
        nullable=False
    )

    stage = Column(
        String,
        nullable=False
    )

    access_token = Column(
        UUID(as_uuid=True),
        nullable=False,
        unique=True,
        index=True
    )

    email = Column(
        String,
        nullable=True
    )

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False
    )

    opened_at = Column(
        DateTime(timezone=True),
        nullable=True
    )

    completed_at = Column(
        DateTime(timezone=True),
        nullable=True
    )

    expires_at = Column(
        DateTime(timezone=True),
        nullable=True
    )