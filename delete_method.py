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

@app.delete("/developers/{dev_id}", status_code=204)
async def delete_developer(dev_id: UUID):

    data = load_data()
    new_data = [dev for dev in data if dev['id'] != str(dev_id)]
    if len(new_data) == len(data):
        raise HTTPException(status_code=404, detail="Developer not found")
    
    save_data(new_data)
    return None