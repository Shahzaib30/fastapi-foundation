from __future__ import annotations

from fastapi import APIRouter, HTTPException

from app.schemas import ProjectClassifyRequest, ProjectClassifyResponse, SpamClassifyRequest, SpamClassifyResponse
from app.services.ml import ProjectClassifierService, SpamClassificationService

router = APIRouter(prefix="/ml", tags=["ML"])

project_service = ProjectClassifierService()
spam_service = SpamClassificationService()


@router.post("/project-classify", response_model=ProjectClassifyResponse)
async def classify_project(payload: ProjectClassifyRequest):
    try:
        return project_service.predict(payload.description)
    except FileNotFoundError as exc:
        raise HTTPException(status_code=503, detail=f"Project classifier artifact missing: {exc}") from exc


@router.post("/spam-classify", response_model=SpamClassifyResponse)
async def classify_spam(payload: SpamClassifyRequest):
    try:
        return spam_service.predict(payload.message)
    except FileNotFoundError as exc:
        raise HTTPException(status_code=503, detail=f"Spam detector artifact missing: {exc}") from exc
