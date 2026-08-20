from sqlalchemy import (
    CheckConstraint,
    Column,
    Date,
    Integer,
    DateTime,
    UniqueConstraint,
    func,
)

from database import Base


class EvaluationCycle(Base):

    __tablename__ = "evaluation_cycles"

    __table_args__ = (
        UniqueConstraint(
            "year",
            "quarter",
            name="uq_evaluation_cycles_year_quarter",
        ),
        CheckConstraint(
            "quarter BETWEEN 1 AND 4",
            name="ck_evaluation_cycles_quarter",
        ),
    )

    id = Column(
        Integer,
        primary_key=True,
        index=True,
    )

    year = Column(
        Integer,
        nullable=False,
        index=True,
    )

    quarter = Column(
        Integer,
        nullable=False,
    )

    start_date = Column(
        Date,
        nullable=False,
    )

    end_date = Column(
        Date,
        nullable=False,
    )

    invitation_date = Column(
        Date,
        nullable=True,
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