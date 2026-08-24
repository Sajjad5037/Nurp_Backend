from sqlalchemy import (
    Column,
    Integer,
    String,
    DateTime,
    Boolean,
    func
)

from database import Base


class Employee(Base):

    __tablename__ = "employees"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    full_name = Column(
        String,
        nullable=False
    )

    email = Column(
        String,
        nullable=False,
        unique=True,
        index=True
    )

    slack_id = Column(
        String,
        nullable=True
    )

    department = Column(
        String,
        nullable=True
    )

    designation = Column(
        String,
        nullable=True
    )

    role = Column(
        String,
        nullable=False,
        default="Employee"
    )

    is_existing_employee = Column(
        Boolean,
        nullable=False,
        default=False
    )
    is_active = Column(Boolean, nullable=False, default=True)

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