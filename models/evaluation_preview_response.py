from sqlalchemy import (
    Column,
    DateTime,
    Integer,
    JSON,
    String,
    func,
)

from database import Base


class EvaluationPreviewResponse(Base):

    __tablename__ = "evaluation_preview_responses"

    id = Column(
        Integer,
        primary_key=True,
        index=True,
    )

    workflow_id = Column(
        String,
        nullable=False,
        unique=True,
        index=True,
    )

    preview_responses = Column(
        JSON,
        nullable=False,
        default=dict,
    )

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )

    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )
