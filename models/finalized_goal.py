from sqlalchemy import (
    Column,
    Date,
    DateTime,
    ForeignKey,
    ForeignKeyConstraint,
    Index,
    Integer,
    Numeric,
    String,
    Text,
    UniqueConstraint,
)

from database import Base


class FinalizedGoal(Base):

    __tablename__ = "finalized_goals"

    __table_args__ = (
        ForeignKeyConstraint(
            ["source_assignment_id", "employee_id"],
            [
                "evaluation_assignments.id",
                "evaluation_assignments.employee_id",
            ],
            name="fk_finalized_goals_source_assignment_employee",
        ),
        UniqueConstraint(
            "source_assignment_id",
            "sequence",
            name="uq_finalized_goals_source_assignment_sequence",
        ),
        Index(
            "ix_finalized_goals_source_assignment_id",
            "source_assignment_id",
        ),
        Index(
            "ix_finalized_goals_employee_id",
            "employee_id",
        ),
    )

    id = Column(
        Integer,
        primary_key=True,
        index=True,
    )

    source_assignment_id = Column(
        Integer,
        nullable=False,
    )

    employee_id = Column(
        Integer,
        ForeignKey("employees.id"),
        nullable=False,
    )

    evaluation_cycle_id = Column(
        Integer,
        ForeignKey("evaluation_cycles.id"),
        nullable=True,
    )

    sequence = Column(
        Integer,
        nullable=False,
    )

    title = Column(
        String,
        nullable=True,
    )

    description = Column(
        Text,
        nullable=False,
    )

    expectation = Column(
        Text,
        nullable=True,
    )

    success_criteria = Column(
        Text,
        nullable=True,
    )

    target_date = Column(
        Date,
        nullable=True,
    )

    weight = Column(
        Numeric(10, 2),
        nullable=True,
    )

    finalized_at = Column(
        DateTime(timezone=True),
        nullable=False,
    )
