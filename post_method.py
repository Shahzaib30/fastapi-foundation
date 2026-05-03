import json
from uuid import UUID
from fastapi import FastAPI, Request, HTTPException
from typing import List

from pydantic import Field
from pydantic_u import BaseModel, EmailStr

app = FastAPI()
file = "developers.json"

class ProjectModel(BaseModel):
    title: str = Field(...)
    client_name: str = Field(...)
    budget: float = Field(..., gt=0)
    is_completed: bool = Field(default=False)

class DeveloperSummary(BaseModel):
    message: str
    project_count: int
    total_value: float = Field(default=0.0)

class DeveloperModel(BaseModel):
    id: UUID = Field(...)
    name: str = Field(...)
    email: EmailStr = Field(...)
    skills: List[str] = Field(...)
    Current_projects: List[ProjectModel] = Field(...) 
    website: str = Field(default=None)

def load_data():
    try:
        with open(file, "r") as f:
            return json.load(f)
    except (json.JSONDecodeError, FileNotFoundError):
        return []
    
def save_data(data):
    with open(file, "w") as f:
        json.dump(data, f)


@app.post("/developers/", response_model=List[DeveloperSummary])
async def create_developer(developer: List[DeveloperModel]):
    all_developers = load_data()
    summaries = []

    for dev in developer:
        total_budget = sum(p.budget for p in dev.Current_projects)
        dev_dict = dev.dict()
        dev_dict["id"] = str(dev_dict["id"])
        all_developers.append(dev_dict)

        summaries.append(DeveloperSummary(
            message=f"Developer {dev.name} has {len(dev.Current_projects)} projects with a total budget of {total_budget}.",
            project_count=len(dev.Current_projects),
            total_value=total_budget
        ))

    save_data(all_developers)
    return summaries