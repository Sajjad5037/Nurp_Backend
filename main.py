from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="FlowPilot Backend",
    version="1.0.0",
    description="Backend API for FlowPilot Workflow Designer"
)

# -------------------------------------------------------------------
# CORS
# -------------------------------------------------------------------

origins = [
    "http://localhost:3000",   # Create React App
    "http://localhost:5173",   # Vite
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],          # Change this later in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# -------------------------------------------------------------------
# Root
# -------------------------------------------------------------------

@app.get("/")
def root():
    return {
        "message": "FlowPilot Backend Running",
        "status": "ok"
    }


# -------------------------------------------------------------------
# Health Check
# -------------------------------------------------------------------

@app.get("/health")
def health():
    return {
        "healthy": True
    }


# -------------------------------------------------------------------
# Evaluation Templates (Temporary)
# -------------------------------------------------------------------

fake_db = []


@app.get("/evaluation-templates")
def get_templates():
    return fake_db


@app.post("/evaluation-templates")
def save_template(template: dict):

    fake_db.append(template)

    return {
        "message": "Template saved successfully.",
        "template": template
    }