from sqlalchemy import (
    Column,
    Integer,
    String,
    DateTime,
    func
)
from sqlalchemy.dialects.postgresql import JSONB

from database import Base


class EvaluationTemplate(Base):

    __tablename__ = "evaluation_templates"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    name = Column(
        String,
        nullable=False
    )

    workflow_json = Column(
        JSONB,
        nullable=False
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
    status = Column(
        String,
        nullable=False,
        default="draft"
    )
    version = Column(
        Integer,
        nullable=False,
        default=1
    )