from __future__ import annotations

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routers.developers import router as developers_router
from app.routers.health import router as health_router
from app.routers.ml import router as ml_router
from app.routers.users import router as users_router
from app.routers.workflows import router as workflows_router


app = FastAPI(
    title="FastAPI Foundation",
    version="0.1.0",
    description="A professional FastAPI foundation with JSON-backed demos, ML endpoints, and LangGraph workflows.",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health_router)
app.include_router(users_router)
app.include_router(developers_router)
app.include_router(ml_router)
app.include_router(workflows_router)
