import json
from typing import List
from uuid import UUID

from fastapi import FastAPI
from pydantic import BaseModel, EmailStr, Field


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
        with open(file, "r", encoding="utf-8") as handle:
            return json.load(handle)
    except (json.JSONDecodeError, FileNotFoundError):
        return []


def save_data(data):
    with open(file, "w", encoding="utf-8") as handle:
        json.dump(data, handle)


@app.post("/developers/", response_model=List[DeveloperSummary])
async def create_developer(developer: List[DeveloperModel]):
    all_developers = load_data()
    summaries = []

    for dev in developer:
        total_budget = sum(project.budget for project in dev.Current_projects)
        dev_dict = dev.model_dump()
        dev_dict["id"] = str(dev_dict["id"])
        all_developers.append(dev_dict)

        summaries.append(
            DeveloperSummary(
                message=f"Developer {dev.name} has {len(dev.Current_projects)} projects with a total budget of {total_budget}.",
                project_count=len(dev.Current_projects),
                total_value=total_budget,
            )
        )

    save_data(all_developers)
    return summaries
