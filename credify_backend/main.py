from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from core.config import settings
from database.mongo import db
from routers import auth_user, auth_admin, aa, scoring, applications, admin, reports
from agent import agent_routes

app = FastAPI(title=settings.PROJECT_NAME)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Database Connection Events
@app.on_event("startup")
def startup_db_client():
    db.connect()

@app.on_event("shutdown")
def shutdown_db_client():
    db.close()

# Routers
app.include_router(auth_user.router, prefix="/auth_user", tags=["User Auth"])
app.include_router(auth_admin.router, prefix="/auth_admin", tags=["Admin Auth"])
app.include_router(aa.router, prefix="/aa", tags=["Account Aggregator"])
app.include_router(scoring.router, prefix="/scoring", tags=["Scoring"])
app.include_router(applications.router, prefix="/applications", tags=["Applications"])
app.include_router(admin.router, prefix="/admin", tags=["Admin"])
app.include_router(reports.router, prefix="/reports", tags=["Reports"])
app.include_router(agent_routes.router, prefix="/agent", tags=["Agent"])


@app.get("/")
def root():
    return {"message": "Welcome to Credify Backend"}


