from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from database import Base, engine
from routers.evaluation_templates import router as evaluation_template_router

# Import the model so SQLAlchemy knows about it
from models.evaluation_template import EvaluationTemplate

app = FastAPI(
    title="FlowPilot Backend",
    version="1.0.0",
    description="Backend API for FlowPilot Workflow Designer"
)

# -------------------------------------------------------------
# Create Database Tables
# -------------------------------------------------------------

Base.metadata.create_all(bind=engine)

# -------------------------------------------------------------
# CORS
# -------------------------------------------------------------

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# -------------------------------------------------------------
# Register Routers
# -------------------------------------------------------------

app.include_router(evaluation_template_router)

# -------------------------------------------------------------
# Root
# -------------------------------------------------------------

@app.get("/")
def root():

    return {

        "message": "FlowPilot Backend Running",

        "status": "ok"

    }


# -------------------------------------------------------------
# Health
# -------------------------------------------------------------

@app.get("/health")
def health():

    return {

        "healthy": True

    }