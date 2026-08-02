from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from dotenv import load_dotenv
import os

# ---------------------------------------------------
# Load .env
# ---------------------------------------------------

load_dotenv()

# ---------------------------------------------------
# Database URL
# ---------------------------------------------------

DATABASE_URL = os.getenv("DATABASE_URL")

if DATABASE_URL is None:

    raise RuntimeError(

        "DATABASE_URL not found in environment variables."

    )

# Railway sometimes uses postgres:// instead of postgresql://

DATABASE_URL = DATABASE_URL.replace(

    "postgres://",

    "postgresql://",

    1

)

# ---------------------------------------------------
# Engine
# ---------------------------------------------------

engine = create_engine(

    DATABASE_URL,

    pool_pre_ping=True

)

# ---------------------------------------------------
# Session
# ---------------------------------------------------

SessionLocal = sessionmaker(

    autocommit=False,

    autoflush=False,

    bind=engine

)

# ---------------------------------------------------
# Base
# ---------------------------------------------------

Base = declarative_base()

# ---------------------------------------------------
# Dependency
# ---------------------------------------------------

def get_db():

    db = SessionLocal()

    try:

        yield db

    finally:

        db.close()