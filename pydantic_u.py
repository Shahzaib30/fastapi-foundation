from pydantic import BaseModel, Field, EmailStr
from typing import List, Optional, Literal
from uuid import UUID

from fastapi import FastAPI, HTTPException, status
import json


# AI Project Management System
class Experience(BaseModel):
    role : Literal["Junior", "Mid", "Senior"]
    experience_year : int

class ProjectList(BaseModel):
    title : str
    is_deployed : bool
    accuracy : Optional[float] = None

class User(BaseModel):
    id : UUID
    username : str = Field(..., min_length= 3, max_length=15)
    email : EmailStr
    experience : List[Experience]
    projects : List[ProjectList]



exp = Experience(role="Senior", experience_year=5)
project = ProjectList(title="AI Chatbot", is_deployed=True, accuracy=0.95)

user = User(
    id=UUID("123e4567-e89b-12d3-a456-426614174000"),
    username="john_doe",
    email = "john.doe@example.com",
    experience=[exp],
    projects=[project]
)


# Scenerio 2 : The Freelance Hub 

class ProjectModel(BaseModel):
    title : str = Field(...)
    client_name : str = Field(...)
    budget : float = Field(..., gt=0)
    is_completed : bool = Field(default=False)

class DeveloperModel(BaseModel):
    id : UUID
    name : str = Field(...)
    email : EmailStr
    skills : List[str]
    current_projects : List[ProjectModel]
    website : Optional[str] = None

class DeveloperSummary(BaseModel):
    message : str
    project_count : int
    total_value : Optional[float] = None

app = FastAPI()

@app.post("/developers", response_model=DeveloperSummary) 
async def get_grand_total(developer_list: List[DeveloperModel]):
    grand_total = 0
    total_projects = 0
    
    for dev in developer_list:
        grand_total += sum(p.budget for p in dev.current_projects)
        total_projects += len(dev.current_projects)
    

    return DeveloperSummary(
        message=f"Total value for all {len(developer_list)} developers processed.",
        project_count=total_projects,
        total_value=grand_total
    )