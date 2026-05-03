import json
from uuid import UUID
from fastapi import FastAPI, Request, HTTPException
from typing import List

from pydantic import Field
from pydantic_u import BaseModel, DeveloperSummary, EmailStr

app = FastAPI()
file = "developers.json"

class ProjectModel(BaseModel):
    title: str = Field(...)
    client_name: str = Field(...)
    budget: float = Field(..., gt=0)
    is_completed: bool = Field(default=False)

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

@app.put("/developers/{dev_id}", response_model=DeveloperModel)
async def update_developer(dev_id: UUID, updated_developer: DeveloperModel):
    data = load_data()

    for index ,dev in enumerate(data):
        if dev['id'] == str(dev_id):
            new_dev_dict = updated_developer.model_dump()
            new_dev_dict["id"] = str(dev_id)
            data[index] = new_dev_dict

            save_data(data)
            return updated_developer
    print("Developer not found")
    raise HTTPException(status_code=404, detail="Developer not found")