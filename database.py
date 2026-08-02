from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import os

# ------------------------------------------------------------------
# Database URL
#
# Local Example:
# postgresql://postgres:password@localhost:5432/flowpilot
#
# Railway Example:
# DATABASE_URL will automatically be available as an environment variable.
# ------------------------------------------------------------------

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://postgres:password@localhost:5432/flowpilot"
)

# ------------------------------------------------------------------
# SQLAlchemy Engine
# ------------------------------------------------------------------

engine = create_engine(

    DATABASE_URL,

    pool_pre_ping=True

)

# ------------------------------------------------------------------
# Session Factory
# ------------------------------------------------------------------

SessionLocal = sessionmaker(

    autocommit=False,

    autoflush=False,

    bind=engine

)

# ------------------------------------------------------------------
# Base Model
# ------------------------------------------------------------------

Base = declarative_base()

# ------------------------------------------------------------------
# Dependency
# ------------------------------------------------------------------

def get_db():

    db = SessionLocal()

    try:

        yield db

    finally:

        db.close()