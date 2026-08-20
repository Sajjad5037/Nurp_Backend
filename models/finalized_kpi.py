from sqlalchemy import (
    Column,
    DateTime,
    ForeignKey,
    ForeignKeyConstraint,
    Index,
    Integer,
    String,
    Text,
    UniqueConstraint,
)

from database import Base


class FinalizedKPI(Base):

    __tablename__ = "finalized_kpis"

    __table_args__ = (
        ForeignKeyConstraint(
            ["source_assignment_id", "employee_id"],
            [
                "evaluation_assignments.id",
                "evaluation_assignments.employee_id",
            ],
            name="fk_finalized_kpis_source_assignment_employee",
        ),
        UniqueConstraint(
            "source_assignment_id",
            "sequence",
            name="uq_finalized_kpis_source_assignment_sequence",
        ),
        Index(
            "ix_finalized_kpis_source_assignment_id",
            "source_assignment_id",
        ),
        Index(
            "ix_finalized_kpis_employee_id",
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

    sequence = Column(
        Integer,
        nullable=False,
    )

    title = Column(
        String,
        nullable=False,
    )

    expectation = Column(
        Text,
        nullable=False,
    )

    finalized_at = Column(
        DateTime(timezone=True),
        nullable=False,
    )
