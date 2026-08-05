from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from database import Base, engine
from routers.evaluation_templates import router as evaluation_template_router
from routers.employees import router as employee_router
from routers.evaluation_master_sheet import router as evaluation_master_sheet_router
from routers.evaluation_assignment import (
    router as evaluation_assignment_router
)
from routers.meeting_readiness import router as meeting_readiness_router

# Import the model so SQLAlchemy knows about it
from models.evaluation_template import EvaluationTemplate
from models.employee import Employee


from models.evaluation_assignment import EvaluationAssignment
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
app.include_router(employee_router)
app.include_router(evaluation_assignment_router)
app.include_router(evaluation_master_sheet_router)
app.include_router(meeting_readiness_router)
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