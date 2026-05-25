from __future__ import annotations

from typing import List, Optional
from uuid import UUID

from pydantic import BaseModel, EmailStr, Field


class ProjectItem(BaseModel):
    title: str = Field(...)
    client_name: str = Field(...)
    budget: float = Field(..., gt=0)
    is_completed: bool = Field(default=False)


class DeveloperBase(BaseModel):
    name: str = Field(...)
    email: EmailStr = Field(...)
    skills: List[str] = Field(default_factory=list)
    current_projects: List[ProjectItem] = Field(default_factory=list)
    website: Optional[str] = None


class DeveloperCreate(DeveloperBase):
    id: UUID = Field(...)


class DeveloperUpdate(DeveloperBase):
    id: UUID = Field(...)


class DeveloperRecord(DeveloperCreate):
    pass


class DeveloperSummary(BaseModel):
    message: str
    project_count: int
    total_value: float = Field(default=0.0)


class ProjectClassifyRequest(BaseModel):
    description: str


class ProjectClassifyResponse(BaseModel):
    project_type: str
    confidence: Optional[float] = None


class SpamClassifyRequest(BaseModel):
    message: str


class SpamClassifyResponse(BaseModel):
    prediction: str
    score: Optional[float] = None


class ProposalRequest(BaseModel):
    project_goal: str


class ProposalResponse(BaseModel):
    developer: str
    proposal: str


class WorkflowProposalResponse(BaseModel):
    draft: str
    critique: str
    final_output: str


class UserProfile(BaseModel):
    id: UUID
    username: str
    email: EmailStr
    is_active: bool = True
    profile: Optional[dict] = None
    technical_stack: List[str] = Field(default_factory=list)
    projects: List[dict] = Field(default_factory=list)
    settings: Optional[dict] = None
    login_history: List[dict] = Field(default_factory=list)
